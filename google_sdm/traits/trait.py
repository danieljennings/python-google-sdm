from abc import abstractstaticmethod, ABC


class Trait(ABC):
    @abstractstaticmethod
    def name():
        pass

    def __init__(self, subself, props, trait_dict):
        for key in props.keys():
            if props[key] in trait_dict:
                setattr(subself, key, trait_dict[props[key]])

                def getter():
                    return getattr(subself, key)
                setattr(subself, key[1::], getter)
            else:
                setattr(subself, key, None)

    def __repr__(self):
        return f"{self.name()}{vars(self)}"
