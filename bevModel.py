import typing

import dataclasses

# co2 kg/litre for burning diesel
# https://carbonpositivelife.com/co2-per-litre-diesel/
dieselBurningEmisions = 2.64

################################################################################
# CO2/kwh emisions to make a battery, low and high
# https://www.ivl.se/download/18.14d7b12e16e3c5c36271070/1574923989017/C444.pdf
batteryManufacturingEmissionsPerKwH = [61, 106]

################################################################################
bestConsumption = 1.8 # stated kWh per mile as stated by Tesla
elonLyingFactor = 2 # how much leeway we are allowing for bev consumption

################################################################################
# lifetime range, a millions miles, in km
lifeTimeRange = 1600000

################################################################################
@dataclasses.dataclass
class BevParams :
    kwhPerKm : float               # how many kWhs user to move one km
    batteryEmmisionsPerkWh : float # kgs of CO2 to make 1kWh of battery
    rangeKM : float = 500 * 1.6      # desired range of vehicle in kms

    # commercial electricity prices, as a small business
    # https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/875777/QEP_Q4_2019.pdf
    price : float = 15 # in pence, per kWh

    # battery pack energy density kwh/kg, based of real world Model 3 figures
    # https://insideevs.com/news/338105/tesla-model-3-battery-cell-has-worlds-highest-energy-density/
    energyDensity: float = 0.207

    # kg CO2 per kWh for electricity generation
    # https://www.rensmart.com/Calculators/KWH-to-CO2
    co2PerKwH = 0.283

    @property
    def batteryCapacity(self) -> float :
        """How big is the battery in kWh."""
        return self.rangeKM * self.kwhPerKm

    @property
    def batteryMass(self) -> float :
        """How heavy is the battery in kg."""
        return self.batteryCapacity / self.energyDensity

    @property
    def manufacturingEmmissions(self) -> float :
        """How may kgs of carbon are emitted to make the battery."""
        return self.batteryCapacity * self.batteryEmmisionsPerkWh

    @property
    def emissionsPerKm(self) -> float :
        """How many kgs of CO2 are emmitted to drive 1km."""
        return self.kwhPerKm * self.co2PerKwH

    @property
    def costPerKm(self) -> float :
        """How many pence to drive 1km for fuel."""
        return self.kwhPerKm * self.price


################################################################################
@dataclasses.dataclass
class DieselParams :
    # Litres/100km for a 40t diesel truck + trailer
    # https://www.volvotrucks.com/content/dam/volvo/volvo-trucks/markets/global/pdf/our-trucks/Emis_eng_10110_14001.pdf
    fuelConsumption : float = 48

    # well to tank CO2 emissions per litre of diesel
    # https://innovationorigins.com/producing-gasoline-and-diesel-emits-more-co2-than-we-thought/
    productionEmissions: float = 0.64

    # cost of diesel per litre (RAC)
    # https://www.rac.co.uk/drive/advice/fuel-watch/
    price = 112

    @property
    def dieselEmissionsPerLitre(self) -> float :
        """How many kgs of CO2 are emitted by litre of fuel burnt."""
        return dieselBurningEmisions + self.productionEmissions

    @property
    def emissionsPerKm(self) -> float :
        """How many kgs of CO2 are emmitted to drive 1km."""
        return self.fuelConsumption * self.dieselEmissionsPerLitre/100

    @property
    def costPerKm(self) -> float :
        """How many pence to drive 1km for fuel."""
        return self.fuelConsumption/100 * self.price

# our default diesel rig params
diesel = DieselParams()

################################################################################
def runModel(bev: BevParams,
             diesel: DieselParams,
             lifeTimeRange: float) -> None :
    bevEmissions    = bev.emissionsPerKm * lifeTimeRange + bev.manufacturingEmmissions
    bevFuelCost     = bev.costPerKm * lifeTimeRange
    dieselFuelCost  = diesel.costPerKm * lifeTimeRange
    dieselEmissions = diesel.emissionsPerKm * lifeTimeRange

    # how many kms would a diesel truck drive to emit
    # the same amount of CO2 emitted in the manfacture of the battery
    equivKmsPerBattery = bev.manufacturingEmmissions/diesel.emissionsPerKm

    print(f"  BEV    : {bev}")
    print(f"  DIESEL : {diesel}")
    print(f"  battery size : {bev.batteryCapacity:,.0f}kWh")
    print(f"  battery mass : {bev.batteryMass:,.0f}kg")
    print(f"  battery CO2 production cost : {bev.manufacturingEmmissions:,.0f}kg")
    print(f"  kms that a diesel truck would drive to emit a battery's worth of CO2 : {equivKmsPerBattery:,.0f}km")
    print(f"  BEV driven + manufacturing CO2 emissions : {bevEmissions:,.0f}kg")
    print(f"  DIESEL driven CO2 emissions : {dieselEmissions:,.0f}kg")
    print(f"  BEV fuel cost : £{bevFuelCost/100:,.0f}")
    print(f"  DIESEL fuel cost : £{dieselFuelCost/100:,.0f}")
    print(f"  CO2 savings  : {100 - 100 * bevEmissions/dieselEmissions:,.0f}%")
    print(f"  Fuel savings : {100 - 100 * bevFuelCost/dieselFuelCost:,.0f}%")


################################################################################
print(f"Over a lifetime range of {lifeTimeRange}")
for k in [bestConsumption, elonLyingFactor * bestConsumption] :
    for b in batteryManufacturingEmissionsPerKwH:
        print("################################################################################")
        bev = BevParams(kwhPerKm = k/1.6,
                        batteryEmmisionsPerkWh = b)
        runModel(bev, diesel, lifeTimeRange)
