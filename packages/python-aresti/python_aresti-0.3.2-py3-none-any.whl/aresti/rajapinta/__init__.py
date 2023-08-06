

class Rajapinta(
  RestYhteys,
  metaclass=RajapinnanTyyppi,
):
  Nakyma = Nakyma

  @staticmethod
  def sanoma(cls):
    return dataclass(
      functools.wraps(cls, updated=())(
        type(cls.__name__, (cls, RestSanoma), {})
      )
    )
    # def sanoma

  @staticmethod
  def yksio(cls):
    return Nakyma.yksio(cls)

  @staticmethod
  def vierasavain(*args, **kwargs):
    return Vierasavain(*args, **kwargs)

  def polku_oletus(self, nakyma):
    return nakyma.__name__.lower() + '/'

  def rajapintakohtainen_nakyma(self, nakyma):
    nakyma_meta = getattr(nakyma, 'Meta', None)
    @functools.wraps(nakyma, updated=())
    class _Nakyma(nakyma, Nakyma):
      class Meta(*((nakyma_meta, ) if nakyma_meta else ()), Nakyma.Meta):
        rajapinta = self
        if nakyma_meta is None or not hasattr(nakyma_meta, 'polku'):
          polku = self.polku_oletus(nakyma)
        # class Meta
      if nakyma_meta is not None:
        Meta = functools.wraps(nakyma_meta, updated=())(Meta)
      # class _Nakyma
    _Nakyma.__annotations__.setdefault(
      _Nakyma.Meta.primaariavain, str
    )
    return dataclass(_Nakyma)
    # def rajapintakohtainen_nakyma

  def __getattribute__(self, avain):
    '''
    Asetetaan Rajapinnan määreinä määriteltyihin
    ``dataclass``-alaluokkiin (näkymät) `Meta.rajapinta`-määre.
    '''
    arvo = super().__getattribute__(avain)
    if isinstance(arvo, type) and is_dataclass(arvo):
      return self.rajapintakohtainen_nakyma(arvo)
    return arvo
    # def __getattribute__

  # class Rajapinta
