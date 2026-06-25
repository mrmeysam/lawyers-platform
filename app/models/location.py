# app/models/location.py
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Province(Base):
    __tablename__ = "provinces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    
    # Relationships
    counties = relationship("County", back_populates="province", cascade="all, delete-orphan")

class County(Base):
    __tablename__ = "counties"
    __table_args__ = (
        UniqueConstraint('name', 'province_id', name='uq_county_name_province'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    province = relationship("Province", back_populates="counties")
    districts = relationship("District", back_populates="county", cascade="all, delete-orphan")

class District(Base):
    __tablename__ = "districts"
    __table_args__ = (
        UniqueConstraint('name', 'county_id', name='uq_district_name_county'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    county_id = Column(Integer, ForeignKey("counties.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    county = relationship("County", back_populates="districts")
    cities = relationship("City", back_populates="district", cascade="all, delete-orphan")

class City(Base):
    __tablename__ = "cities"
    __table_args__ = (
        UniqueConstraint('name', 'district_id', name='uq_city_name_district'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    district = relationship("District", back_populates="cities")
