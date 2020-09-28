# coding: utf-8

"""
WARNING: used by FAB, but logic uses version in nw_logic.
The primary copy is nw_logic -- copy changes here.



on relationships...
  * declare them in the parent (not child), eg, for Order:
  *    OrderDetailList = relationship("OrderDetail", backref="OrderHeader", cascade_backrefs=True)

"""
import sqlalchemy_utils
from sqlalchemy import Boolean, Column, DECIMAL, DateTime, Float, ForeignKey, Integer, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.testing import db

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'Category'

    Id = Column(Integer, primary_key=True)
    CategoryName = Column(String(8000))
    Description = Column(String(8000))


class Customer(Base):
    __tablename__ = 'Customer'

    Id = Column(String(8000), primary_key=True)
    CompanyName = Column(String(8000))
    ContactName = Column(String(8000))
    ContactTitle = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    Phone = Column(String(8000))
    Fax = Column(String(8000))
    Balance = Column(DECIMAL)
    CreditLimit = Column(DECIMAL)
    OrderCount = Column(Integer)
    UnpaidOrderCount = Column(Integer)

    #  OrderList = relationship("Order", cascade_backrefs=True)  # backref="Customer", FIXME cleanup
    OrderList = relationship("Order", cascade_backrefs=True, backref="Customer")


class CustomerDemographic(Base):
    __tablename__ = 'CustomerDemographic'

    Id = Column(String(8000), primary_key=True)
    CustomerDesc = Column(String(8000))


class Employee(Base):
    __tablename__ = 'Employee'

    Id = Column(Integer, primary_key=True)
    LastName = Column(String(8000))
    FirstName = Column(String(8000))
    Title = Column(String(8000))
    TitleOfCourtesy = Column(String(8000))
    BirthDate = Column(String(8000))
    HireDate = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    HomePhone = Column(String(8000))
    Extension = Column(String(8000))
    Photo = Column(LargeBinary)
    Notes = Column(String(8000))
    # ReportsTo = Column(Integer)
    ReportsTo = Column(ForeignKey('Employee.Id'), nullable=False)
    PhotoPath = Column(String(8000))

    OrderList = relationship("Order", cascade_backrefs=True, backref="SalesRep")
    # https://stackoverflow.com/questions/2638217/sqlalchemy-mapping-self-referential-relationship-as-one-to-many-declarative-f
    Manager = relationship('Employee', remote_side='Employee.Id',
                                      backref='Manages')  # parent Company

# not sure about this... adding backref="Order" causes this failure:  FIXME cleanup
# "Error creating backref 'Employee' on relationship 'Employee.OrderList':
#   property of that name exists on mapper 'mapped class Order->Order'"

class Product(Base):
    __tablename__ = 'Product'

    Id = Column(Integer, primary_key=True)
    ProductName = Column(String(8000))
    SupplierId = Column(Integer, nullable=False)
    CategoryId = Column(Integer, nullable=False)
    QuantityPerUnit = Column(String(8000))
    UnitPrice = Column(DECIMAL, nullable=False)
    UnitsInStock = Column(Integer, nullable=False)
    UnitsOnOrder = Column(Integer, nullable=False)
    ReorderLevel = Column(Integer, nullable=False)
    Discontinued = Column(Integer, nullable=False)
    UnitsShipped = Column(Integer, nullable=False)

    OrderList = relationship("OrderDetail", cascade_backrefs=True, backref="ProductOrdered")



class Region(Base):
    __tablename__ = 'Region'

    Id = Column(Integer, primary_key=True)
    RegionDescription = Column(String(8000))


class Shipper(Base):
    __tablename__ = 'Shipper'

    Id = Column(Integer, primary_key=True)
    CompanyName = Column(String(8000))
    Phone = Column(String(8000))


class Supplier(Base):
    __tablename__ = 'Supplier'

    Id = Column(Integer, primary_key=True)
    CompanyName = Column(String(8000))
    ContactName = Column(String(8000))
    ContactTitle = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    Phone = Column(String(8000))
    Fax = Column(String(8000))
    HomePage = Column(String(8000))


class Territory(Base):
    __tablename__ = 'Territory'

    Id = Column(String(8000), primary_key=True)
    TerritoryDescription = Column(String(8000))
    RegionId = Column(Integer, nullable=False)


class CustomerCustomerDemo(Base):
    __tablename__ = 'CustomerCustomerDemo'

    Id = Column(String(8000), primary_key=True)
    CustomerTypeId = Column(ForeignKey('Customer.Id'))

    Customer = relationship('Customer')


class EmployeeTerritory(Base):
    __tablename__ = 'EmployeeTerritory'

    Id = Column(String(8000), primary_key=True)
    EmployeeId = Column(ForeignKey('Employee.Id'), nullable=False)
    TerritoryId = Column(ForeignKey('Territory.Id'))

    Employee = relationship('Employee')
    Territory = relationship('Territory')


class Order(Base):
    __tablename__ = 'Order'

    Id = Column(Integer, primary_key=True)  #, autoincrement=True)
    CustomerId = Column(ForeignKey('Customer.Id'))
    EmployeeId = Column(ForeignKey('Employee.Id'))
    OrderDate = Column(String(8000))
    RequiredDate = Column(String(8000))
    ShippedDate = Column(String(8000))
    ShipVia = Column(Integer)
    Freight = Column(DECIMAL, nullable=False)
    ShipName = Column(String(8000))
    ShipAddress = Column(String(8000))
    ShipCity = Column(String(8000))
    ShipRegion = Column(String(8000))
    ShipPostalCode = Column(String(8000))
    ShipCountry = Column(String(8000))
    AmountTotal = Column(DECIMAL)

    OrderDetailList = relationship("OrderDetail", backref="OrderHeader", cascade_backrefs=True)


class OrderDetail(Base):
    __tablename__ = 'OrderDetail'

    Id = Column(Integer, primary_key=True)  #, autoincrement=True)
    OrderId = Column(ForeignKey('Order.Id'), nullable=False)
    ProductId = Column(ForeignKey('Product.Id'), nullable=False)
    UnitPrice = Column(DECIMAL, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Discount = Column(Float, nullable=False)
    Amount = Column(DECIMAL)
    ShippedDate = Column(String(8000))

    # Order = relationship('Order', back_populates="OrderDetailList")  FIXME cleanup
    # Product = relationship('Product')



class AbPermission(Base):
    __tablename__ = 'ab_permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class AbRegisterUser(Base):
    __tablename__ = 'ab_register_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256))
    email = Column(String(64), nullable=False)
    registration_date = Column(DateTime)
    registration_hash = Column(String(256))


class AbRole(Base):
    __tablename__ = 'ab_role'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)


class AbUser(Base):
    __tablename__ = 'ab_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256))
    active = Column(Boolean)
    email = Column(String(64), nullable=False, unique=True)
    last_login = Column(DateTime)
    login_count = Column(Integer)
    fail_login_count = Column(Integer)
    created_on = Column(DateTime)
    changed_on = Column(DateTime)
    created_by_fk = Column(ForeignKey('ab_user.id'))
    changed_by_fk = Column(ForeignKey('ab_user.id'))

    parent = relationship('AbUser', remote_side=[id], primaryjoin='AbUser.changed_by_fk == AbUser.id')
    parent1 = relationship('AbUser', remote_side=[id], primaryjoin='AbUser.created_by_fk == AbUser.id')


class AbViewMenu(Base):
    __tablename__ = 'ab_view_menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)

class AbPermissionView(Base):
    __tablename__ = 'ab_permission_view'
    __table_args__ = (
        UniqueConstraint('permission_id', 'view_menu_id'),
    )

    id = Column(Integer, primary_key=True)
    permission_id = Column(ForeignKey('ab_permission.id'))
    view_menu_id = Column(ForeignKey('ab_view_menu.id'))

    permission = relationship('AbPermission')
    view_menu = relationship('AbViewMenu')


class AbUserRole(Base):
    __tablename__ = 'ab_user_role'
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('ab_user.id'))
    role_id = Column(ForeignKey('ab_role.id'))

    role = relationship('AbRole')
    user = relationship('AbUser')


class AbPermissionViewRole(Base):
    __tablename__ = 'ab_permission_view_role'
    __table_args__ = (
        UniqueConstraint('permission_view_id', 'role_id'),
    )

    id = Column(Integer, primary_key=True)
    permission_view_id = Column(ForeignKey('ab_permission_view.id'))
    role_id = Column(ForeignKey('ab_role.id'))

    permission_view = relationship('AbPermissionView')
    role = relationship('AbRole')

