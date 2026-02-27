from rest_framework import exceptions

class TenantMixin:
    def get_queryset(self):
        user = self.request.user
        
        if not user.workplace:
            raise exceptions.ValidationError('You dont have a workplace attached to your account.')
        
        queryset = super().get_queryset()
        return queryset.filter(workplace=user.workplace)


class OwnershipPermissionMixin:
    workplace_not_found_msg = 'You do not have a current workplace.'
    not_workplace_owner_msg = 'Only the owner can perform this action.'

    def perform_destroy(self, instance):
        if not self.request.user.workplace:
            raise exceptions.ValidationError(self.workplace_not_found_msg)
        if self.request.user != self.request.user.workplace.owner:
            raise exceptions.ValidationError(self.not_workplace_owner_msg)
        return super().perform_destroy(instance)

    def perform_update(self, instance):
        if not self.request.user.workplace:
            raise exceptions.ValidationError(self.workplace_not_found_msg)
        if self.request.user != self.request.user.workplace.owner:
            raise exceptions.ValidationError(self.not_workplace_owner_msg)
        return super().perform_update(instance)