from datetime import datetime
from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean, Float, Date, JSON, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Kraj(db.Model):
    __tablename__ = 'kraje'

    id = Column(Unicode, primary_key=True)
    nazev = Column(Unicode)


class Okres(db.Model):
    __tablename__ = 'okresy'

    id = Column(Unicode, primary_key=True)
    nazev = Column(Unicode)
    kraj_id = Column(Unicode, ForeignKey('kraje.id'))

    kraj = relationship("Kraj", back_populates="okresy")

    def __repr__(self):
        return "<Okres(nazev='%s')>" % (self.nazev)


Kraj.okresy = relationship("Okres", back_populates="kraj")


class OckovaciMisto(db.Model):
    __tablename__ = 'ockovaci_mista'

    id = Column(Unicode, primary_key=True)
    nazev = Column(Unicode)
    okres_id = Column(Unicode, ForeignKey('okresy.id'))
    status = Column(Boolean)
    adresa = Column(Unicode)
    latitude = Column(Float)
    longitude = Column(Float)
    nrpzs_kod = Column(Unicode)
    minimalni_kapacita = Column(Integer)
    bezbarierovy_pristup = Column(Boolean)
    service_id = Column(Integer)
    operation_id = Column(Integer)
    odkaz = Column(Unicode)

    okres = relationship("Okres", back_populates="ockovaci_mista")

    def __repr__(self):
        return "<OckovaciMisto(nazev='%s', service_id=%s, operation_id=%s)>" % (
        self.nazev, self.service_id, self.operation_id)


Okres.ockovaci_mista = relationship("OckovaciMisto", back_populates="okres")


class Import(db.Model):
    __tablename__ = 'importy'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, default=datetime.now())
    status = Column(Unicode)

    def __repr__(self):
        return "<Import(id=%s, start='%s', status='%s')>" % (self.id, self.start, self.status)


class VolnaMistaCas(db.Model):
    __tablename__ = 'volna_mista_cas'

    id = Column(Integer, primary_key=True)
    import_id = Column(Integer, ForeignKey('importy.id'))
    cas_ziskani = Column(DateTime, default=datetime.now())
    misto_id = Column(Unicode, ForeignKey('ockovaci_mista.id'))
    datum = Column(Date)
    cas = Column(Unicode)
    start = Column(DateTime)
    volna_mista = Column(Integer)
    place_id = Column(Integer)
    user_service_id = Column(Integer)

    import_ = relationship('Import', back_populates='volna_mista_cas')
    misto = relationship('OckovaciMisto', back_populates='volna_mista_cas')

    def __repr__(self):
        return "<VolnaMistaCas(misto_id='%s', cas='%s', volna_mista=%s)>" % (
        self.misto_id, self.start, self.volna_mista)


Import.volna_mista_cas = relationship("VolnaMistaCas", back_populates="import_")
OckovaciMisto.volna_mista_cas = relationship("VolnaMistaCas", back_populates="misto")


class VolnaMistaDen(db.Model):
    __tablename__ = 'volna_mista_den'

    id = Column(Integer, primary_key=True)
    import_id = Column(Integer, ForeignKey('importy.id'))
    cas_ziskani = Column(DateTime, default=datetime.now())
    misto_id = Column(Unicode, ForeignKey('ockovaci_mista.id'))
    datum = Column(Date)
    volna_mista = Column(Integer)
    data = Column(JSON)

    import_ = relationship('Import', back_populates='volna_mista_den')
    misto = relationship('OckovaciMisto', back_populates='volna_mista_den')

    def __repr__(self):
        return "<VolnaMistaDen(misto_id='%s', datum='%s', volna_mista=%s)>" % (
        self.misto_id, self.datum, self.volna_mista)


Import.volna_mista_den = relationship("VolnaMistaDen", back_populates="import_")
OckovaciMisto.volna_mista_den = relationship("VolnaMistaDen", back_populates="misto")


class OckovaniSpotreba(db.Model):
    __tablename__ = 'ockovani_spotreba'

    datum = Column(Date, primary_key=True)
    ockovaci_misto_id = Column(Unicode, ForeignKey('ockovaci_mista.id'), primary_key=True)
    ockovaci_misto_nazev = Column(Unicode)
    kraj_nuts_kod = Column(Unicode)
    kraj_nazev = Column(Unicode)
    ockovaci_latka = Column(Unicode, primary_key=True)
    vyrobce = Column(Unicode)
    pouzite_ampulky = Column(Integer)
    znehodnocene_ampulky = Column(Integer)

    misto = relationship('OckovaciMisto', back_populates='ockovani_spotreba')

    def __repr__(self):
        return "<VaccineConsumption(ockovaci_misto_nazev='%s', datum='%s', ockovaci_latka=%s, pouzite_ampulky=%s)>" % (
        self.ockovaci_misto_nazev, self.datum, self.ockovaci_latka, self.pouzite_ampulky)


OckovaciMisto.ockovani_spotreba = relationship("OckovaniSpotreba", back_populates="misto")


class OckovaniDistribuce(db.Model):
    __tablename__ = 'ockovani_distribuce'

    datum = Column(Date, primary_key=True)
    ockovaci_misto_id = Column(Unicode, ForeignKey('ockovaci_mista.id'), primary_key=True)
    ockovaci_misto_nazev = Column(Unicode)
    kraj_nuts_kod = Column(Unicode)
    kraj_nazev = Column(Unicode)
    cilove_ockovaci_misto_id = Column(Unicode, primary_key=True)
    cilove_ockovaci_misto_nazev = Column(Unicode)
    cilovy_kraj_kod = Column(Unicode)
    cilovy_kraj_nazev = Column(Unicode)
    ockovaci_latka = Column(Unicode, primary_key=True)
    vyrobce = Column(Unicode)
    akce = Column(Unicode, primary_key=True)
    pocet_ampulek = Column(Integer)

    misto = relationship('OckovaciMisto', back_populates='ockovani_distribuce')

    def __repr__(self):
        return "<VaccineDistribution(ockovaci_misto_nazev='%s', cilove_ockovaci_misto_nazev='%s', datum='%s', ockovaci_latka=%s, pocet_ampulek=%s)>" % (
        self.ockovaci_misto_nazev, self.cilove_ockovaci_misto_nazev, self.datum, self.ockovaci_latka, self.pocet_ampulek)


OckovaciMisto.ockovani_distribuce = relationship("OckovaniDistribuce", back_populates="misto")
