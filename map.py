from room import Room

# TODO: Define items, locked, etc
# create each room
vault_entrance = Room("Vault Entrance")
decon = Room("Decontamination")
security = Room("Security")
storage = Room("Storage")
atrium = Room("Atrium")
east_wing = Room("East Wing")
cafeteria = Room("Cafeteria")
living_quarters = Room("Living Quarters")
medical = Room("Medical")
emergency_response = Room("Emergency Response")
armory = Room("Armory")
west_wing = Room("West Wing")
chemical = Room("Chemical")
experimental = Room("Experimental")
r_and_d = Room("R&D")

# connect rooms together
# Vault Entrance
vault_entrance.connect("south", decon)

# Decon
decon.connect("north", vault_entrance)
decon.connect("south", atrium)
decon.connect("east", security)
decon.connect("west", storage)

# Storage
storage.connect("east", decon)

# Security
security.connect("west", decon)

# Atrium
atrium.connect("north", decon)
atrium.connect("south", emergency_response)
atrium.connect("east", east_wing)
atrium.connect("west", west_wing)

# East Wing
east_wing.connect("north", medical)
east_wing.connect("south", cafeteria)
east_wing.connect("east", living_quarters)
east_wing.connect("west", atrium)

# Medical
medical.connect("south", east_wing)

# Cafeteria
cafeteria.connect("north", east_wing)

# Living Quarters
living_quarters.connect("west", east_wing)

# Emergency Response
emergency_response.connect("north", atrium)
emergency_response.connect("south", armory)

# Armory
armory.connect("north", emergency_response)

# West Wing
west_wing.connect("north", chemical)
west_wing.connect("south", experimental)
west_wing.connect("east", atrium)
west_wing.connect("west", r_and_d)

# Chemical
chemical.connect("south", west_wing)

# Experimental
experimental.connect("north", west_wing)

# Research and Development
r_and_d.connect("east", west_wing)

# Set starting room for the player
starting_room = vault_entrance