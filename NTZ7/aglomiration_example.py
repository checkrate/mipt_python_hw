from person import Person
from family import Family
from city import City

class Agglomeration:
    def __init__(self, name, max_count_residents):
        self.__name = name
        self.__max_count_residents = max_count_residents
        self.__current_count_residents = 0
        self.__residents = list()
        self.__families = list()
        self.__cities = list()

    def add_person(self, name, surname, midname, city_name):
        try:
            city_found = False
            for city in self.__cities:
                if city_name == city.get_name():
                    city_found = True
                    person = Person(name, surname, midname, city_name)
                    city.add_person(name, surname, midname)
                    self.__residents.append(person)
                    self.__current_count_residents += 1
                    break
            if not city_found:
                raise ValueError(f"City '{city_name}' not found in agglomeration.")
        except Exception as e:
            print(f"Error adding person: {e}")

    def remove_person(self, name, surname, midname, city_name):
        try:
            city_found = False
            for city in self.__cities:
                if city.get_name() == city_name:
                    city_found = True
                    for resident in self.__residents:
                        if resident.get_city() != city_name:
                            continue
                        if (resident.get_name() == name and resident.get_surname() == surname 
                                and resident.get_midname() == midname):
                            self.__residents.remove(resident)
                            city.remove_person(name, surname, midname)
                            return
                    raise ValueError(f"Resident '{name} {surname} {midname}' not found in city '{city_name}'.")
            if not city_found:
                raise ValueError(f"City '{city_name}' not found in agglomeration.")
        except Exception as e:
            print(f"Error removing person: {e}")

    def add_family(self, name, husband, wife, city_name=''):
        try:
            husband_ = None
            wife_ = None
            for resident in self.__residents:
                if husband == resident.__str__():
                    husband_ = resident
                elif wife == resident.__str__():
                    wife_ = resident
            if husband_ is None or wife_ is None:
                raise ValueError(f"Either husband '{husband}' or wife '{wife}' not found among residents.")
            self.__families.append(Family(name, husband_, wife_))
        except Exception as e:
            print(f"Error adding family: {e}")

    def add_children(self, family_name, children):
        try:
            family_found = False
            for family in self.__families:
                if family.get_name() == family_name:
                    family_found = True
                    family.add_children(children)
                    break
            if not family_found:
                raise ValueError(f"Family '{family_name}' not found.")
        except Exception as e:
            print(f"Error adding children to family: {e}")

    def add_city(self, name, count):
        try:
            if (self.__current_count_residents + count) > self.__max_count_residents:
                raise ValueError("Adding this city would exceed the maximum count of residents.")
            self.__cities.append(City(name, count))
        except Exception as e:
            print(f"Error adding city: {e}")

    def get_cities(self):
        try:
            return self.__cities
        except Exception as e:
            print(f"Error retrieving cities: {e}")
            return []

    def get_families(self):
        try:
            return self.__families
        except Exception as e:
            print(f"Error retrieving families: {e}")
            return []
