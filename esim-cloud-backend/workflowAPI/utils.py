from rest_framework.response import Response
from rest_framework import status as http_status
import uuid
from .serializers import StatusSerializer
from .models import  Permission, State, Transition, Permission
from publishAPI.models import  TransitionHistory

def ChangeStatus(self, status, project):
    if isinstance(project.project_id, uuid.UUID):
        try:
            user_roles = self.request.user.groups.all()
        except:
            return Response(data={'message': 'No User Role'}, status=http_status.HTTP_404_NOT_FOUND)
        if project.author == self.request.user and Permission.objects.filter(role__in=user_roles, view_own_states=project.state).exists():
            pass
        elif project.author != self.request.user and Permission.objects.filter(role__in=user_roles, view_other_states=project.state).exists():
            pass
        else:
            return Response(status=http_status.HTTP_401_UNAUTHORIZED)
        circuit_transition = Transition.objects.get(from_state=project.state,
                                                    to_state=State.objects.get(name=status))
        roles = circuit_transition.role.all()
        if circuit_transition.from_state != project.state:
            return Response({'error': 'You are not authorized to edit the status.'},
                            status=http_status.HTTP_401_UNAUTHORIZED)
        else:
            if circuit_transition.only_for_creator is True and self.request.user == project.author:
                transition_history = TransitionHistory(project_id=project.project_id,
                                                       transition_author=self.request.user,
                                                       from_state=project.state,
                                                       reviewer_notes='',
                                                       to_state=circuit_transition.to_state)
                transition_history.save()
                project.state = circuit_transition.to_state
                project.save()
                print(project.state)
                print("Saved in changed status")
                state = project.state
                serialized = StatusSerializer(state)
                return Response(serialized.data)
            elif circuit_transition.only_for_creator is False:
                roles_set = set(roles)
                user_roles_set = set(user_roles)
                if user_roles_set.intersection(roles_set):
                    intersection = user_roles_set.intersection(roles_set)
                    for user_role in intersection:
                        if user_role.customgroup.is_arduino is project.is_arduino:
                            if circuit_transition.restricted_for_creator is True and project.author == self.request.user:
                                return Response({'error': 'You are not authorized to edit the status as it is not allowed for creator.'},
                                                status=http_status.HTTP_401_UNAUTHORIZED)
                            else:
                                transition_history = TransitionHistory(project_id=project.project_id,
                                                                       transition_author=self.request.user,
                                                                       from_state=project.state,
                                                                       reviewer_notes='',
                                                                       to_state=circuit_transition.to_state)
                                transition_history.save()
                                project.state = circuit_transition.to_state
                                project.save()
                                state = project.state
                                serialized = StatusSerializer(state)
                                return Response(serialized.data)
                    return Response({'error': 'You are not authorized to edit the status as you dont have the role'},
                                    status=http_status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'error': 'You are not authorized to edit the status as you dont have the role.'},
                                    status=http_status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'You are not authorized to edit the status as it is only allowed for creator.'},
                                status=http_status.HTTP_401_UNAUTHORIZED)
