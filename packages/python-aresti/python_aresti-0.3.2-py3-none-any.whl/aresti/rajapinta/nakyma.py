from dataclasses import dataclass, is_dataclass
import functools

from aresti.sanoma import RestSanoma
from aresti.tyokalut import (
  luokka_tai_oliometodi,
  luokkamaare,
)
from aresti.rest import RestYhteys

from .meta import RajapinnanTyyppi


class Nakyma(RestSanoma):

  def __init__(self, rajapinta, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.rajapinta = rajapinta
    # def __init__

  class Meta:
    rajapinta: 'Rajapinta'
    polku: str
    primaariavain: str = 'id'
    @luokkamaare
    def crud(cls) -> dict:
      # pylint: disable=no-self-argument
      return {
        'nouda_kaikki': f'{cls.polku}',
        'nouda': f'{cls.polku}/%(avain)s',
        'lisaa': f'{cls.polku}',
        'muuta': f'{cls.polku}/%(avain)s',
        'tuhoa': f'{cls.polku}/%(avain)s',
      }

  @luokka_tai_oliometodi
  async def nouda(cls) -> ['Nakyma']:
    # pylint: disable=no-self-argument
    return [
      cls.saapuva(sanoma)
      for sanoma in await cls.Meta.rajapinta.nouda_sivutettu_data(
        cls.Meta.crud['nouda_kaikki']
      )
    ]
    # async def nouda

  @nouda.oliometodi
  async def nouda(self) -> 'Nakyma':
    ''' Päivitä ``self`` rajapinnasta. '''
    assert (avain := getattr(self, self.Meta.primaariavain, False))
    haettu = self.saapuva(
      await self.Meta.rajapinta.nouda_data(
        self.Meta.crud['nouda'] % {'avain': avain}
      )
    )
    self.__dict__.update(haettu.__dict__)
    return self
    # async def nouda

  async def lisaa(self):
    if getattr(self, self.Meta.primaariavain, False):
      return await self.muuta()
    await self.Meta.rajapinta.lisaa_data(
      self.Meta.crud['lisaa'],
      self.lahteva()
    )
    # async def lisaa

  async def muuta(self):
    assert (avain := getattr(self, self.Meta.primaariavain, False))
    await self.Meta.rajapinta.muuta_data(
      self.Meta.crud['muuta'] % {'avain': avain},
      self.lahteva()
    )
    # async def muuta

  async def tuhoa(self):
    assert (avain := getattr(self, self.Meta.primaariavain, False))
    await self.Meta.rajapinta.tuhoa_data(
      self.Meta.crud['tuhoa'] % {'avain': avain},
    )
    # async def tuhoa

  @staticmethod
  def yksio(cls):
    ''' Merkitse REST-näkymä yksittäiseen riviin rajoittuvaksi. '''
    @functools.wraps(cls, updated=())
    class Yksio(cls):
      class Meta(*(
        (cls.Meta, ) if hasattr(cls, 'Meta') else ()
      ), Nakyma.Meta):
        crud = {
          'nouda': f'{cls.Meta.polku}',
          'lisaa': f'{cls.Meta.polku}',
        }
      @luokka_tai_oliometodi
      async def nouda(cls) -> 'Yksio':
        # pylint: disable=no-member
        return cls.saapuva(await cls.Meta.rajapinta.nouda_data(
          cls.Meta.crud['nouda']
        ))
        # async def nouda

      @nouda.oliometodi
      async def nouda(self) -> 'Yksio':
        haettu = self.saapuva(
          await self.Meta.rajapinta.nouda_data(
            self.Meta.crud['nouda']
          )
        )
        self.__dict__.update(haettu.__dict__)
        return self
        # async def nouda

      async def muuta(self):
        await self.Meta.rajapinta.lisaa_data(
          self.Meta.crud['lisaa'],
          self.lahteva()
        )
        # async def muuta

      async def toimintoa_ei_ole(self):
        raise RuntimeError('Toiminto ei mahdollinen')

      lisaa = tuhoa = toimintoa_ei_ole
      # class Yksio
    return Yksio
    # def yksio

  def __getattribute__(self, avain):
    '''
    Asetetaan Näkymän määreinä määriteltyihin
    ``dataclass``-alaluokkiin (sisemmät näkymät)
    `Meta.rajapinta`-määre.
    '''
    print('tässä', self, avain)
    arvo = super().__getattribute__(avain)
    if isinstance(arvo, type) and is_dataclass(arvo):
      return self.Meta.rajapinta.rajapintakohtainen_nakyma(arvo)
    return arvo
    # def __getattribute__

  # class Nakyma
