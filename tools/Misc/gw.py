# auto_runner.py
from thull import thull

# List of missing engine/motor sizes (meters)
missing_cases = [
    # Micro / MEMS / molecular motors
    ("auto_molecular_motor_1e-09m", 1e-9),
    ("auto_piezo_1e-09m", 1e-9),
    ("auto_electrostatic_MEMS_1e-09m", 1e-9),
    ("auto_molecular_motor_1e-08m", 1e-8),
    ("auto_piezo_1e-08m", 1e-8),
    ("auto_electrostatic_MEMS_1e-08m", 1e-8),
    ("auto_molecular_motor_1e-07m", 1e-7),
    ("auto_piezo_1e-07m", 1e-7),
    ("auto_electrostatic_MEMS_1e-07m", 1e-7),
    ("auto_piezo_1e-06m", 1e-6),
    ("auto_micro_BLDC_1e-06m", 1e-6),
    ("auto_micro_flywheel_1e-06m", 1e-6),
    ("auto_piezo_1e-05m", 1e-5),
    ("auto_micro_BLDC_1e-05m", 1e-5),
    ("auto_micro_flywheel_1e-05m", 1e-5),
    ("auto_piezo_0.0001m", 1e-4),
    ("auto_micro_BLDC_0.0001m", 1e-4),
    ("auto_micro_flywheel_0.0001m", 1e-4),

    # Small engines and actuators
    ("auto_small_BLDC_0.001m", 0.001),
    ("auto_compressed_gas_0.001m", 0.001),
    ("auto_spring_0.001m", 0.001),
    ("auto_small_capacitor_pulse_0.001m", 0.001),
    ("auto_small_BLDC_0.005m", 0.005),
    ("auto_compressed_gas_0.005m", 0.005),
    ("auto_spring_0.005m", 0.005),
    ("auto_small_capacitor_pulse_0.005m", 0.005),
    ("auto_small_BLDC_0.01m", 0.01),
    ("auto_compressed_gas_0.01m", 0.01),
    ("auto_spring_0.01m", 0.01),
    ("auto_small_capacitor_pulse_0.01m", 0.01),
    ("auto_small_ICE_0.05m", 0.05),
    ("auto_battery_motor_0.05m", 0.05),
    ("auto_coilgun_micro_0.05m", 0.05),
    ("auto_small_ICE_0.1m", 0.1),
    ("auto_battery_motor_0.1m", 0.1),
    ("auto_coilgun_micro_0.1m", 0.1),
    ("auto_small_ICE_0.2m", 0.2),
    ("auto_battery_motor_0.2m", 0.2),
    ("auto_coilgun_micro_0.2m", 0.2),
    ("auto_small_ICE_0.5m", 0.5),
    ("auto_battery_motor_0.5m", 0.5),
    ("auto_coilgun_micro_0.5m", 0.5),

    # Automotive / mid-sized
    ("auto_automotive_ICE_1m", 1),
    ("auto_automotive_electric_1m", 1),
    ("auto_small_coilgun_1m", 1),
    ("auto_flywheel_storage_1m", 1),
    ("auto_automotive_ICE_2m", 2),
    ("auto_automotive_electric_2m", 2),
    ("auto_small_coilgun_2m", 2),
    ("auto_flywheel_storage_2m", 2),
    ("auto_automotive_ICE_3m", 3),
    ("auto_automotive_electric_3m", 3),
    ("auto_small_coilgun_3m", 3),
    ("auto_flywheel_storage_3m", 3),
    ("auto_automotive_ICE_5m", 5),
    ("auto_automotive_electric_5m", 5),
    ("auto_small_coilgun_5m", 5),
    ("auto_flywheel_storage_5m", 5),
    ("auto_automotive_ICE_8m", 8),
    ("auto_automotive_electric_8m", 8),
    ("auto_small_coilgun_8m", 8),
    ("auto_flywheel_storage_8m", 8),

    # Large engines / turbines
    ("auto_turbo_ICE_10m", 10),
    ("auto_gas_turbine_10m", 10),
    ("auto_hydraulic_accumulator_10m", 10),
    ("auto_turbo_ICE_15m", 15),
    ("auto_gas_turbine_15m", 15),
    ("auto_hydraulic_accumulator_15m", 15),
    ("auto_turbo_ICE_20m", 20),
    ("auto_gas_turbine_20m", 20),
    ("auto_hydraulic_accumulator_20m", 20),
    ("auto_large_turbine_30m", 30),
    ("auto_multi_engine_plant_30m", 30),
    ("auto_railgun_30m", 30),
    ("auto_capacitor_bank_30m", 30),
    ("auto_large_turbine_44m", 44),
    ("auto_multi_engine_plant_44m", 44),
    ("auto_railgun_44m", 44),
    ("auto_capacitor_bank_44m", 44),
    ("auto_large_turbine_60m", 60),
    ("auto_multi_engine_plant_60m", 60),
    ("auto_railgun_60m", 60),
    ("auto_capacitor_bank_60m", 60),
    ("auto_powerplant_grid_100m", 100),
    ("auto_orbital_EM_launcher_100m", 100),
    ("auto_multiple_coil_array_100m", 100),
]

# Run all cases
for name, L in missing_cases:
    try:
        print(f"\n--- Running {name} (length={L} m) ---")
        tt = thull(name, L, 1, 0)
        tt = tt.init()
        tt.getfric()
    except Exception as e:
        print(f"[ERROR] {name} failed: {e}")