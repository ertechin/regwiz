changes = [
    {
        "path": r"HARDWARE\DESCRIPTION\System",
        "values": {
            "SystemBiosVersion": "INTEL  - 6040000"
        }
    },
    {
        "path": r"HARDWARE\DESCRIPTION\System\BIOS",
        "values": {
            "BIOSVendor": "MSI, Inc."
        }
    },
    {
        "path": r"SYSTEM\ControlSet001\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
        "values": {
            "DriverDesc": "AMD Radeon SVGA 3D",
            "HardwareInformation.AdapterString": "AMD Radeon SVGA 3D",
            "HardwareInformation.BiosString": "n/a",
            "HardwareInformation.ChipType": "AMD Radeon Graphics Processor (0x6811)",
            "HardwareInformation.DacType": "Internal DAC(400MHZ)",
            "ProviderName": "AMD, Inc."
        }
    },
    {
        "path": r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
        "values": {
            "DriverDesc": "AMD Radeon SVGA 3D",
            "HardwareInformation.AdapterString": "AMD Radeon SVGA 3D",
            "HardwareInformation.BiosString": "n/a",
            "HardwareInformation.ChipType": "AMD Radeon Graphics Processor (0x6811)",
            "HardwareInformation.DacType": "Internal DAC(400MHZ)",
            "ProviderName": "AMD, Inc."
        }
    }, 
    {
        "path": r"SYSTEM\HardwareConfig\Current",
        "values": {
            "BIOSVendor": "MSI, Inc.",
            "SystemBiosVersion": "INTEL  - 6040000"
        }
    }, 
    {
        "static_base_path": r"SYSTEM\HardwareConfig",
        "after_dynamic_path": "",
        "values": {
            "BIOSVendor": "MSI, Inc.",
            "SystemBiosVersion": "INTEL  - 6040000"
        }
    }
] + [
        {
            "static_base_path": r"SYSTEM\CurrentControlSet\Control\Video",
            "after_dynamic_path": f"000{i}",
            "values": {
                "DriverDesc": "AMD Radeon SVGA 3D",
                "HardwareInformation.AdapterString": "AMD Radeon SVGA 3D",
                "HardwareInformation.BiosString": "n/a",
                "HardwareInformation.ChipType": "AMD Radeon Graphics Processor (0x6811)",
                "HardwareInformation.DacType": "Internal DAC(400MHZ)",
                "ProviderName": "AMD, Inc. E"
            }
        } for i in range(8)
] + [
        {
            "static_base_path": r"SYSTEM\ControlSet001\Control\Video",
            "after_dynamic_path": f"000{i}",
            "values": {
                "DriverDesc": "AMD Radeon SVGA 3D",
                "HardwareInformation.AdapterString": "AMD Radeon SVGA 3D",
                "HardwareInformation.BiosString": "n/a",
                "HardwareInformation.ChipType": "AMD Radeon Graphics Processor (0x6811)",
                "HardwareInformation.DacType": "Internal DAC(400MHZ)",
                "ProviderName": "AMD, Inc. E"
            }
        } for i in range(8)
]