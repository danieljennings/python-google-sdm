from .trait import Trait


def SDMTraitGetter(trait_type):
    def wrap(func):
        def inner(self, **kwargs):
            trait_name = trait_type.name()
            kwargs['trait'] = trait_type(self.traits[trait_name])
            return func(self, **kwargs)
        return inner
    return wrap
