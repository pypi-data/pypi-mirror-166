import dataclasses
import enum
import typing

from whocan import _policies


PermissionDefiner = typing.Union[_policies.Policy, 'PolicySet']


class Operation(enum.Enum):
    """The manner in which policies should be merged."""
    UNION = 'union'
    INTERSECT = 'intersect'


@dataclasses.dataclass
class PolicySet:
    """A set of policies that interact to determine access."""

    policies: typing.List[PermissionDefiner]
    operation: Operation = Operation.INTERSECT

    def is_allowed(
            self,
            action: str,
            resource: str = None,
            principal: str = None,
            arguments: typing.Dict[str, str] = None
    ) -> bool:
        """
        Determine if the given policy allows the specified action on the
        specified resource.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            Whether the action is allowed on the resource.
        """
        return 'allow' == self.evaluate(action, resource, principal, arguments)

    def evaluate(
            self,
            action: str,
            resource: str = None,
            principal: str = None,
            arguments: typing.Dict[str, str] = None
    ) -> typing.Optional[str]:
        """
        Evaluate the policy to determine if it allows, denys, or makes no
        comment on the specified resource and action.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            Either "allow", "deny" or None.
        """
        evaluations = [
            policy.evaluate(action, resource, principal, arguments)
            for policy in self.policies
        ]
        if any(v == 'deny' for v in evaluations):
            return 'deny'
        handler = all if (self.operation==Operation.INTERSECT) else any
        if handler(v == 'allow' for v in evaluations):
            return 'allow'
        return None

    def to_jsonable(self) -> dict:
        """Serialize the policy set to a JSONable object."""
        return {
            'type': 'policy_set',
            'operation': self.operation.value,
            'policies': [p.to_jsonable() for p in self.policies],
        }

    @classmethod
    def from_jsonable(cls, jsonable: dict) -> dict:
        """Deserialize the policy set from a JSONable object."""
        operation = {
            k.value: k
            for k in Operation
        }[jsonable['operation']]
        policies = [
            _policies.Policy.from_jsonable(p)
            if p['type'] == 'policy' else
            PolicySet.from_jsonable(p)
            for p in jsonable['policies']
        ]
        return cls(policies, operation)