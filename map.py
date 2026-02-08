from room import Room
from utils import GREEN, RESET, YELLOW


def build_map():
    """Creates the rooms and their connections for the game map."""
    vault_entrance = Room(
        "Vault Entrance",
        "You step through a massive reinforced door into a stale, dimly lit entrance where the outside world feels far away.",
    )

    decon = Room(
        "Decon",
        "You walk into a long decontamination chamber as warning lights flicker and silent vents line the walls.",
    )

    storage = Room(
        "Storage",
        "You step into a cluttered storage room filled with wrecked crates, collapsed shelves, and layers of dust.",
        item="flashlight",
    )

    security = Room(
        "Security",
        "You enter a security room with dead monitors, overturned chairs, and control panels frozen in time.",
        locked=True,
        item="id_tag",
    )

    atrium = Room(
        "Atrium",
        "You step into a wide atrium that serves as the vault's central hub, with corridors branching off in every direction.",
        dark=True,
    )

    east_wing = Room(
        "East Wing",
        "You walk down a long corridor leading toward the living areas, the air feeling quieter the farther you go.",
    )

    medical = Room(
        "Medical",
        "You step into an abandoned medical clinic where scattered supplies and overturned equipment suggest a rushed evacuation.",
        locked=True,
        item="mask",
    )

    cafeteria = Room(
        "Cafeteria",
        "You enter a large cafeteria with long tables and a silent kitchen. A note is taped to the counter.",
        note=(
            "Most of us never made it past the West Wing.\n\n"
            "If you're reading this, you need to be prepared before going any farther.\n\n"
            "The gas leaks in the lower storage areas will choke you without a proper mask. "
            "Radiation in the labs is worse. A mask helps, but you'll need a full HAZMAT suit "
            "to survive prolonged exposure.\n\n"
            "The Armory was sealed after the incident. Keycards won't open it anymore. "
            "The locking mechanism corrodes easily though. Acid should melt it down if you can "
            "get your hands on some.\n\n"
            "Whatever is in Research & Development can't be stopped by weapons alone. "
            "The Radzapper was designed to work only when fully powered and stabilized. "
            "Without the fusion core, identification tag, and proper protection, you are dead meat.\n\n"
            "They said the device was untested.\n\n"
            "If you're going in there, make sure you have everything. There won't be a second chance."
        ),
    )

    living_quarters = Room(
        "Living Quarters",
        "You walk into the living quarters where personal belongings remain scattered across empty dorm rooms.",
        item="keycard",
    )

    emergency_response = Room(
        "Emergency Response",
        "You step into an emergency response area lined with equipment racks and faded instructions on the walls.",
        locked=True,
        item="hazmat_suit",
    )

    armory = Room(
        "Armory",
        "You enter a reinforced armory where weapon racks and protective gear sit locked away behind heavy barriers.",
        locked=True,
        item="radzapper",
    )

    west_wing = Room(
        "West Wing",
        "You walk into a corridor marked with warning signs and lab symbols, hinting at dangerous work once done here.",
        hazard="gas",
    )

    chemical = Room(
        "Chemical",
        "You step into a chemical storage area where broken containers and stained floors make the air burn your throat.",
        hazard="radiation",
        item="acid",
    )

    experimental = Room(
        "Experimental",
        "You enter a ruined laboratory filled with shattered glass, damaged machinery, and failed experiments.",
        hazard="gas",
        item="fusion_core",
    )

    r_and_d = Room(
        "Research & Development",
        "You step into a secured research lab with dark terminals and locked workstations, hiding the vault's most sensitive project.",
        locked=True,
    )

    # Connect rooms
    vault_entrance.connect("south", decon)

    decon.connect("north", vault_entrance)
    decon.connect("south", atrium)
    decon.connect("west", storage)
    decon.connect("east", security)

    storage.connect("east", decon)
    security.connect("west", decon)

    atrium.connect("north", decon)
    atrium.connect("west", west_wing)
    atrium.connect("east", east_wing)
    atrium.connect("south", emergency_response)

    east_wing.connect("west", atrium)
    east_wing.connect("north", medical)
    east_wing.connect("south", cafeteria)
    east_wing.connect("east", living_quarters)

    medical.connect("south", east_wing)
    cafeteria.connect("north", east_wing)
    living_quarters.connect("west", east_wing)

    west_wing.connect("east", atrium)
    west_wing.connect("north", chemical)
    west_wing.connect("south", experimental)
    west_wing.connect("west", r_and_d)

    chemical.connect("south", west_wing)
    experimental.connect("north", west_wing)
    r_and_d.connect("east", west_wing)

    emergency_response.connect("north", atrium)
    emergency_response.connect("south", armory)

    armory.connect("north", emergency_response)

    # Build rooms dict
    rooms = {
        vault_entrance.name: vault_entrance,
        decon.name: decon,
        storage.name: storage,
        security.name: security,
        atrium.name: atrium,
        east_wing.name: east_wing,
        medical.name: medical,
        cafeteria.name: cafeteria,
        living_quarters.name: living_quarters,
        emergency_response.name: emergency_response,
        armory.name: armory,
        west_wing.name: west_wing,
        chemical.name: chemical,
        experimental.name: experimental,
        r_and_d.name: r_and_d,
    }

    return rooms


def print_map() -> None:
    """Prints a simple ASCII map of the vault layout."""
    print(
        f"""{GREEN}
          Vault 166 Map (North is up)
                    [VE]
                    |  |
              [ST]--[DE]--[SE]
                    |  |
              [CH]  |  |  [MD]
        [RD]--[WW]--[AT]--[EW][LQ]
              [EX]  |  |  [CF]
                    [ER]
                    [AR]

        {YELLOW}
        Legend:
        VE: Vault Entrance
        DE: Decon
        ST: Storage
        SE: Security
        AT: Atrium
        EW: East Wing
        MD: Medical
        LQ: Living Quarters
        ER: Emergency Response
        CF: Cafeteria
        AR: Armory
        WW: West Wing
        CH: Chemical
        EX: Experimental
        RD: Research & Development
        {RESET}
         """,
    )
