from dataclasses import dataclass, is_dataclass


@dataclass
class Vierasavain:
  class Meta:
    rajapinta: 'Rajapinta'

  nakyma: str
  vierasavain: str = 'id'

  @type.__call__
  class _nakyma:
    def __get__(self, instance, cls=None):
      nakyma = instance.__dict__['_nakyma'] = getattr(
        instance.Meta.rajapinta,
        instance.nakyma
      )
      return nakyma
      # def __get__
    # class _nakyma

  def lahteva(self, sanoma):
    return {
      self.vierasavain: self._nakyma.lahteva(sanoma)[
        self._nakyma.Meta.primaariavain
      ]
    }

  def saapuva(self, sanoma):
    return self._nakyma.saapuva({
      self._nakyma.Meta.primaariavain: sanoma[self.vierasavain]
    })

  # class Vierasavain
