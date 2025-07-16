# Sampire AIO by Smaptastic - edited by Galeamar
# Weapon ability selection logic largely taken from script by Orion

# Create a dress agent that includes your melee weapon
# Create a dress agent that includes your ranged weapon

from AutoComplete import *
from System import Byte
from System.Collections.Generic import List
import random
import ctypes
from ctypes import wintypes
user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.GetAsyncKeyState.restype = wintypes.SHORT
user32.GetAsyncKeyState.argtypes = [wintypes.INT]


'''
****************************************************************************************************************************
SETTINGS:

Edit the settings below prior to running. It is set up to be reasonably functional out of the box, but it is set up with
my personal settings. You may use different skills than me, so make sure to go through these.

****************************************************************************************************************************
'''

#Run the restart script in rare instance that something is lifted while the script is swapping weapons and the built in no equipped weapon protections fail. True or False
Restart = True

meleedress1 = 'wars side arm' # Whatever your melee Dress List is named
meleename1 = "War's Side Arm" # The name of your melee weapon
meleeserial1 = 0x402FE887 # The name of your melee weapon
meleehand = 'FirstValid' # 'RightHand', 'LeftHand', or 'FirstValid'
meleecustom = True #Is your melee weapon customized or a named weapon(War's Side Arm) True or False
custommeleePrimarySA = 'WW' #'DS' for  double strike or double shot, 'SA' for bleed, ignore armor or infectious strike 'WW' for frenzied whirlwind or whirlwind, 'NA' for none of these
custommeleeSecondarySA = 'SA' #'DS' for  double strike or double shot, 'SA' for bleed, ignore armor or infectious strike 'WW' for frenzied whirlwind or whirlwind, 'NA' for none of these
rangeddress = 'bow' # Whatever your ranged Dress List is named
rangedname = 'yumi' # The namel of your ranged weapon
rangedserial = 0x401A8AE5 # The namel of your ranged weapon
rangedhand = 'FirstValid' # 'RightHand', 'LeftHand', or 'FirstValid'
rangedcustom = False #Is your ranged weapon customized or a named weapon(Thunderbolt) True or False
customrangedPrimarySA = 'WW' #'DS' for  double strike or double shot, 'SA' for bleed, ignore armor or infectious strike 'WW' for frenzied whirlwind or whirlwind, 'NA' for none of these
customrangedSecondarySA = 'DS' #'DS' for  double strike or double shot, 'SA' for bleed, ignore armor or infectious strike 'WW' for frenzied whirlwind or whirlwind, 'NA' for none of these

# If the script starts with an empty hand, it will error out.  Choose meleedress1, rangeddress, or the name of another Dress List.
# But remember if you choose your own Dress List to put the list inside single perenth ie, 'other list name'
starter = meleedress1 

# Do you want to aggro mobs other than the one you're actually fighting? This targets and attacks any mob in a wide radius to draw
# its aggro. Otherwise, you'll just fight the closest target (other mobs may still aggro by other means, like proximity or hit area)
aggroMobs = True

# Combat buffs from Necro, Bushido, and Chivalry (always up in combat, not situational)
# To use multiple buffs, use ["buff1", "buff2"] format. Be sure to put the buffs in the right magic school.
necroCombatBuffs = None # ["Curse Weapon"]
chivCombatBuffs = ["Consecrate Weapon", "Divine Fury"]
bushCombatBuffs = ["Counter Attack"]
masteryCombatBuffs = None # ["Inspire"]
divinefury = True  #True casts Divine Fury False does not
stamcheck = 250 # how much stam to cast divine fury if under for healing/swing speed. this may vary player to player.

# Do you want to honor priority targets?
# This will disregard all other possible honor targets if you have a priority target in range.
honorPriorityTargets = True

# Do you want to use Enemy of One vs priority targets?
# This will use EOO against priority targets if they are completely alone, even if you don't have EOO in chivCombatBuffs.
eooPriorityTargets = True

# Do you want to use Curse Weapon against priority targets?
# This will maintain CW when you're near a priority target, even if you don't have CW in necroCombatBuffs.
curseWeaponPriorityTargets = False

# List of priority targets for Honor, EOO, and CW
priorityTargetList = ["Krampus", "An Annoying Thing", "Rainbow Daemon", "Lord Voldemort", "Nagini", "Harry Potter", "Zaqqum", "Darth", "Emperor", "Gaia", "osiredon the scalis enforcer", "a daemonic kraken", "Water Tentacle", "The Loch Ness Monster", "leviathan", "King of the Bunnies", "April's Fool", "A Leprechaun", "Gello", "Venus", "Indominus Rex", "Aphidia", "The Chess Master", "the Collector", "a frost dragon", "the Lord of", "an Ancient", "Spectre Queen", "Jack Frost", "The Abominable Snowman", "Maleficent", "Dragon", "the harrower", "the true harrower", "The Master", "Abscess", "Morphius", "The Beast", "Gothel", "Wolf", "Gallich", "A Horrible Man", "Ilmodon", "A Tombwing", "Gray Wailer", "Webmouth", "Zhaan", "Thranger", "Flame Daemon", "Scrill", "Grigorus", "Noirkrach", "Pestilence", "Famine", "War", "Dr. Jekyll", "Mr. Hyde", "Hannibal Lecter", "Black Phillip", "Dr. Satan", "Dracula", "Imhotep", "Big Bob", "The Wolfman", "Jason Voorhees", "The Bogeyman", "Michael Myers", "Freddy Krueger", "The Candyman", "The Butcher", "Abaddon", "Carrie", "The Rancor", "Frankenstein's Monster", "King Kong", "a xenomorph", "Godzilla", "Leatherface", "Church", "Valak", "Death", "The Headless Horseman", "Umbria", "Lethe", "Evil Spellbook", "Renowned", "Chaos Vortex", "Chief Paroxysmus", "Putrefier", "Abyssal Infernal", "Abyssmal Horror", "Anon", "Barracoon", "a bone demon", "Charybdis", "Cora the Sorceress", "Corgul", "Ankou", "Arhaios", "Ophis", "Armarus", "Arsat", "Azazel", "Ga'ahp", "Grigorus", "Heksen", "Hrallath", "Karnax", "Keelus", "Kra'an", "Peinsluth", "Peirazo", "Ponerus", "Taet", "Nu'uhn", "Therion", "Turi'el", "Vairocan", "Blassarrabb", "Centibis", "Crenabil", "Farthak", "Flaggroth", "Gragok", "Gragragron", "Grothelfiend", "Krullus", "Krygar", "Laitesach", "Legron", "Lorbna", "Noirkrach", "Pariah", "Thranger", "Vendodroth", "Vilithrar", "Ydoc", "LlessueZhaan", "Dragon Turtle", "Dread Horn", "Drelgor", "Exodus", "Fleshrenderer", "Ilhenir", "Juo'nar", "Khal Ankur", "Lady Melisande", "Lord Oaks", "Medusa", "Mephitis", "Meraktus", "Monstrous Interred Grizzle", "Navrey Night-Eyes", "Neira", "Osiredon", "Ozymandias", "Primeval Lich", "Rikktor", "Semidar", "Shadow Knight", "Astaroth", "Faulinei", "Nosfentor", "Shanty", "Shimmering Effusion", "Silvani", "Slasher of Veils", "Stygian Dragon", "The Harrower", "Travesty", "Twaulo", "Virtuebane", "Zipactriotl", "Cassiel", "Crarigor", "Empalk", "Flandrith", "Gathfe", "Ix", "Magor", "Manglar", "Perfus", "Po-Kor", "Scrill", "Selminus", "Skred", "Slix", "Stavinfeks", "Steelbane", "Verolyn", "Victux", "Vladeer", "Xtul", "Arametheus", "Archatrix", "Doomor", "Erdok", "Helzigar", "Jonar", "Krakus", "Lord Kaos", "Malashim", "Marcus Fel", "Marth'Fador", "Montobulus", "Nelokhiel", "Oghmus", "Samael", "Terxor", "Tyrnak", "Uhn", "Usuhl", "Zul"]

# The max number of mobs you want to aggro at once (if you have aggroed more than this it will stop until some are dead/gone)
# Does not account for mobs that attack you while you already have others aggroed, so you might end up with more.
# Does nothing if aggroMobs is set to False.
aggroCap = 20

# Script only supports untargeted mastery buffs for now. Pet-targeted is tough (due to the gump which I don't know how to handle),
# enemy-targeted is hard to automate (due to having to target the right enemy), and I don't know of any relevant/useful self-targeted buffs.
# Whispering, Inspirne, Invigorate, Resilience, and Perseverance should all work.
# To use multiple buffs, use untargetedMasteryBuffs = ['buff1', 'buff2']
untargetedMasteryBuffs =  None #  ['Invigorate', 'Inspire'] # 

# Constant (even out of combat) buffs from Necro, Bushido, and Chivalry
# To use multiple buffs, use ["buff1", "buff2"] format. Be sure to put the buffs in the right magic school.
necroPermBuffs = ["Vampiric Embrace"] #["Vampiric Embrace"]
chivPermBuffs = None
bushPermBuffs = None
magePermBuffs = ["bless"] # ["Protection"] ["bless"]
removedebuffs = True
hitscheck = 410
closewounds = True #True casts Close Wounds False does not
touchoflife = False #True casts Touch Of Life False does not 
greaterheal = False #True casts Greater Heal False does not

# Train Bushido? Requires using abilities you might not normally use to get it to max.
# Replaces the Bushido combat buffs while training. Once at cap, this does nothing (normal Bushido combat buffs are used instead).
trainBushido = False
bushidoCap = 120

# Kill unicorns? Included exclusively for unicorn farming.
killUnicorns = False
unicornList = ["a unicorn", "a ki-rin"]

# Bank gold? Uses bag of sending to send gold to bank as appropriate.
bankGold = False
# If your gold stack is below this weight, the stash will not trigger no matter what your max weight is.
# Mostly useful if you are getting overloaded with other heavy stuff but don't want to constantly stash.
# This is NOT the max weight your stack is allowed to achieve before stashing.
minBankStackWeight = 130

# Honor targets? (There is no real benefit to turning this off unless another script is screwing it up)
honorTargets = True

# Mana cost of your most expensive permanent buff. I don't have a great way of setting cost per-buff.
permBuffMana = 15

# List of things you don't want to instruct your pet to attack. This does not guarantee they won't attack (due to guard aggro),
# But you won't TELL your pet to attack them at least.
# Also applies to Discord.
dontKillList = ['a horse', 'a reindeer', 'a mule', 'a pack llama', 'a dog', 'a cat', 'cat', 'a dolphin', 'a pack horse']
summonsToIgnore = ["a rising colossus", "a nature's fury", "a blade spirit"]
healersToIgnore = ["healer", "priest of mondain"]
# Strings to check to see if a mobile is someone else's pet.
mobileStrings = ["loyalty", "bonded"]

# These settings all apply to the weapon ability selection logic imported from Orion.
# They are mana costs for your various weapon abilities. Tinker with these as you will. 
wwmana = 28
aimana = 28
msmana = 10
lsmana = 6
dsmana = 30

#Equip your ranged weapon.  The script will error out if your weapon hand is empty.
Dress.ChangeList(starter)
Dress.DressFStart()
Misc.Pause(1000)

''' End of settings'''

if Restart == True:
    Misc.ScriptRun("Sampire AIO Error Recovery.py")


def isMoving():
    return user32.GetAsyncKeyState(0x02) & 0x8000

# Finds all enemies around. Can adjust range and whether you want to attack hostiles only or any gray, as well as range.
# Default settings are attack any gray, 10 range.
def findEnemies(hostilesOnly=True, innocentsIncluded=False, maxRange=10):
    enemyFilter = Mobiles.Filter()
    enemyFilter.RangeMax = maxRange
    if innocentsIncluded:
        enemyFilter.Notorieties = List[Byte](bytes([1, 2, 3, 4, 5, 6]))
    elif not hostilesOnly:
        enemyFilter.Notorieties = List[Byte](bytes([3, 4, 5, 6]))
    else:
        enemyFilter.Notorieties = List[Byte](bytes([4, 5, 6]))
    enemyFilter.IsGhost = False
    enemyFilter.Friend = False
    enemyFilter.CheckLineOfSight = True
    enemyFilter.CheckIgnoreObject = True
    enemyList = []
    enemyList = Mobiles.ApplyFilter(enemyFilter)
    if not enemyList:
        return False
    # So this line is weird, but the list the filter kicks out behaves strangely. Makes it hard to modify, move stuff around, etc.
    # Copying it to a new list seems to fix all that.
    enemyListPython = [x for x in enemyList]
    return enemyListPython

# Removes stuff you don't want to kill from all potential enemies around and returns the result as a list.
# Can adjust range and whether you want to attack hostiles only or any gray, as well as range.
# Default settings are attack any gray, 10 range.
def findTargets(hostilesOnly=True, innocentsIncluded=False, maxRange=10):
    targetList = []
    targetList = findEnemies(hostilesOnly, innocentsIncluded, maxRange)
    if not targetList: # Throw a false if we don't have targets.
        return False
    targetListCopy = targetList[:] # Gonna be deleting stuff in the main list so we need to copy it to a new list to parse.
    for enemy in targetListCopy:
        nextEnemy = False
        if enemy.CanRename: # Remove our pets.
            targetList.remove(enemy)
            continue
        enemyName = enemy.Name.lower()
        enemySerial = enemy.Serial
        if any(noKill in enemyName for noKill in dontKillLower) or any(noSummon in enemyName for noSummon in summonsLower): # Remove stuff we don't want to kill.
            if enemy in targetList:
                targetList.remove(enemy)
            continue
        for healerName in healersLower: # Remove healers.
            if any(healerName in noHealers.lower() for noHealers in Mobiles.GetPropStringList(enemySerial)):
                if enemy in targetList:
                    targetList.remove(enemy)
                nextEnemy = True # Flag that we want to move to the next enemy in the list since we removed this one.
                break
        if nextEnemy:
            continue
        for mobileString in mobileStringsLower: # Remove allies' pets.
            if any(mobileString in petTest.lower() for petTest in Mobiles.GetPropStringList(enemySerial)):
                if enemy in targetList:
                    targetList.remove(enemy)
                nextEnemy = True # Flag that we want to move to the next enemy in the list since we removed this one.
                break
        if nextEnemy:
            continue
        if killUnicorns and enemy.Notoriety <= 2:
            if not any(unicornName in enemyName for unicornName in unicornListLower):
                if enemy in targetList:
                    targetList.remove(enemy)
                continue

    return targetList

# This is for buffs we want on permanently, whether in combat or not.
def buffCheck():
    if Player.Mana < permBuffMana or isMoving():
        return False
    if untargetedMasteryBuffs:
        for b in untargetedMasteryBuffs:
            if Player.BuffsExist(b) or Timer.Check("spellTimer"):
                continue
            Journal.Clear()
            Spells.CastMastery(b)
            if Journal.Search('before you can use'):
                Timer.Create('masteryTimer', 20000)
                Misc.Pause(20)
                return False
            Timer.Create("spellTimer", 4000)
            Misc.Pause(1500)
            return True
    if necroPermBuffs:
        for b in necroPermBuffs:
            if Player.BuffsExist(b) or Timer.Check("spellTimer"):
                continue
            Spells.CastNecro(b)
            Timer.Create("spellTimer", 2000)
            Misc.Pause(1000)
            return True
    if bushPermBuffs:
        for b in bushPermBuffs:
            if Player.BuffsExist(b) or Timer.Check("spellTimer"):
                continue
            Spells.CastBushido(b)
            Timer.Create("spellTimer", 1000)
            Misc.Pause(100)
            return True
    if chivPermBuffs:
        for b in chivPermBuffs:
            if Player.BuffsExist(b) or Timer.Check("spellTimer"):
                continue
            Spells.CastChivalry(b)
            Timer.Create("spellTimer", 1500)
            Misc.Pause(500)
            return True
    if magePermBuffs:
        for b in magePermBuffs:
            if Player.BuffsExist(b) or Timer.Check("spellTimer"):
                continue
            Spells.CastMagery(b,Player.Serial,1500,50)
            Timer.Create("spellTimer", 1500)
            return True
    if Player.BuffsExist('Curse') and removedebuffs:
        Spells.CastChivalry('Remove Curse',Player.Serial,1500,50)
        Timer.Create("spellTimer", 1500)
        return True
    if Player.BuffsExist('Strangle') and removedebuffs:
        Spells.CastChivalry('Remove Curse',Player.Serial,1500,50)
        Timer.Create("spellTimer", 1500)
        return True
    if Player.BuffsExist('Mind Rot') and removedebuffs:
        Spells.CastChivalry('Remove Curse',Player.Serial,1500,50)
        Timer.Create("spellTimer", 1500)
        return True 
    if Player.BuffsExist('Corpse Skin') and removedebuffs:
        Spells.CastChivalry('Remove Curse',Player.Serial,1500,50)
        Timer.Create("spellTimer", 1500)
        return True 
    if Player.BuffsExist('Clumsy') and removedebuffs:
        Spells.CastChivalry('Remove Curse',Player.Serial,1500,50)
        Timer.Create("spellTimer", 1500)
        return True
    if Player.BuffsExist('Feeblemind') and removedebuffs:
        Spells.CastChivalry('Remove Curse',Player.Serial,1500,50)
        Timer.Create("spellTimer", 1500)
        return True 
    if Player.BuffsExist('Weaken') and removedebuffs:
        Spells.CastChivalry('Remove Curse',Player.Serial,1500,50)
        Timer.Create("spellTimer", 1500)
        return True        
    if Player.Hits < hitscheck and closewounds: # if hits is under set hitscheck up top and closewounds setting is set to True at top. 
        Spells.CastChivalry('Close Wounds',Player.Serial,1500,50) #Cast Close Wounds\
        Timer.Create("spellTimer", 1500)
        return True
    if Player.Hits < hitscheck and touchoflife: # if hits is under set hitscheck up top and closewounds setting is set to True at top. 
        Spells.CastCleric('Touch of Life',Player.Serial,1500,50) #Cast Touch of Life\
        Timer.Create("spellTimer", 1500)
        return True
    if Player.Hits < hitscheck and greaterheal: # if hits is under set hitscheck up top and closewounds setting is set to True at top. 
        Spells.Cast('Greater Heal',Player.Serial,1500,50) #Cast Greater Heal\
        Timer.Create("spellTimer", 1500)
        return True
    return False

# This is for buffs we only want to use in combat.
def combatBuffs():
    if Player.Mana < 7: # Kinda arbitrary number but I'm not setting a mana cost per skill.
        return False
    if curseWeaponPriorityTargets and not Player.BuffsExist("Curse Weapon") and nearbyPriorityCheck() and not Timer.Check("spellTimer"):
        Spells.CastNecro("Curse Weapon")
        Timer.Create("spellTimer", 200)
        Misc.Pause(100)
    if bushCombatBuffs and not (trainBushido and Player.GetSkillValue("Bushido") < bushidoCap) and not Timer.Check("bushidoTimer"):
        for b in bushCombatBuffs:
            if Player.BuffsExist(b):
                continue
            Spells.CastBushido(b)
            Timer.Create("bushidoTimer", 200)
            Misc.Pause(100)
            return True
    if chivCombatBuffs and not Timer.Check("spellTimer"):
        for b in chivCombatBuffs:
            if Player.BuffsExist(b):
                continue
            Spells.CastChivalry(b)
            Timer.Create("spellTimer", 200)
            Misc.Pause(100)
            return True
    if Player.Stam < stamcheck and divinefury: # if stam is under set stam check up top and castdivine setting is set to True at top. 
        Spells.CastChivalry('Divine Fury') #Cast Divine Fury\
        Timer.Create("spellTimer", 200)
        Misc.Pause(100) # pause
        return True            
    if necroCombatBuffs and not Timer.Check("spellTimer"):
        for b in necroCombatBuffs:
            if Player.BuffsExist(b):
                continue
            Spells.CastNecro(b)
            Timer.Create("spellTimer", 200)
            Misc.Pause(100)
            return True
    if masteryCombatBuffs and not Timer.Check("spellTimer"):
        for b in masteryCombatBuffs:
            if Player.BuffsExist(b):
                continue
            Spells.CastMastery(b)
            Timer.Create("spellTimer", 200)
            Misc.Pause(100)
            return True
    return False

def masteryBuffsOff():
    if masteryCombatBuffs and not Timer.Check("spellTimer"):
        for b in masteryCombatBuffs:
            if not Player.BuffsExist(b):
                continue
            Spells.CastMastery(b)
            Timer.Create("spellTimer", 200)
            Misc.Pause(100)
            return True
    return False


# Parses the list of possible kill targets and attacks based on various settings.
def findAggroSerial(actualTarget=False, honorOnly=False):
    global currentlyAttacking
    global currentTargetSerial
    global sameTarget
    sameTarget = False
    closestSerial = None
    if currentlyAttacking:
        # First, check to see if every mob in currentlyAttacking is alive and within range. If not, remove it from currentlyAttacking.
        # currentlyAttacking is a list of living mobs we have attacked already (thus drawing their aggro).
        # We cap this list with the aggroCap variable so we can adjust how much heat we want.
        # Stores as a list of serials since those are permanent.
        currentlyAttackingCopy = currentlyAttacking[:]
        for i in currentlyAttackingCopy:
            mobStatusCheck = None
            mobStatusCheck = Mobiles.FindBySerial(i)
            if not mobStatusCheck: # If the mob doesn't exist any more (including if dead), remove it.
                currentlyAttacking.remove(i)
                continue
            if Player.DistanceTo(mobStatusCheck) > 10: # Remove the mob if it has gone too far away.
                currentlyAttacking.remove(i)

    # If we've aggroed less than the max living/nearby creatures, we find the nearest and that will be our target to return.
    # We don't return targets that are already on the list.
    # The target we return is added to the list.
    if len(currentlyAttacking) >= aggroCap: 
        return False
    killList = []
    if honorOnly:
        killList = findTargets(False, killUnicorns, 10)
    elif aggroMobs and not actualTarget: # If we've set aggroMobs, we're pulling enemies from a wide range to draw them in.
        killList = findTargets(False, killUnicorns, 12)
    else:
        killList = findTargets(False, killUnicorns, 10) # If we haven't set aggroMobs, we're just making sure we tag nearby enemies.
    if not killList:
        return False
    
    # Now we start caring about mob distance to player, so we're going to sort killList by distance.
    if not killList: # At this point we might have removed every mob from the list, so we're checking to make sure that's not true.
        return False
    killList.sort(key = lambda x: Player.DistanceTo(x))
    # If we input the actualTarget parameter, we're getting the target we want to actually attack rather than just another target to
    # aggro. We're going to remember the target we're attacking until it dies or leaves melee range.
    if honorOnly:
        for i in killList:
            if i.Hits == i.HitsMax:
                return i.Serial
            continue
        return False
    
    if actualTarget:
        if not currentTargetSerial: # If this is our first target, the nearest mob is now our kill target.
            currentTargetSerial = killList[0].Serial
        currentTarget = Mobiles.FindBySerial(currentTargetSerial) 
        if not currentTarget: # If our kill target died, the closest living mob is now our kill target.
            currentTargetSerial = killList[0].Serial
        elif ((Player.DistanceTo(currentTarget) > 1) and currentTargetSerial != killList[0].Serial): # If our kill target is out of melee range, we find a new kill target.
            currentTargetSerial = killList[0].Serial
        elif currentTarget.WarMode and Target.GetLastAttack() == currentTargetSerial:
            sameTarget = True
        return currentTargetSerial
    
    # This is for if we didn't use the actualTarget parameter. It's just aggroing the nearest thing that needs aggroing.
    # Remember, stuff is already sorted by distance to player.
    for i in killList: # This checks through the list of targets from closest out.
        if not i.WarMode or i.Serial not in currentlyAttacking: # If something isn't war mode or already in currentlyAttacking, that's our target.
            closestSerial = i.Serial
            break
        continue
    if not closestSerial:
        return False # If we didn't find something we're already aggroed on, return a false.
    if closestSerial not in currentlyAttacking:
        currentlyAttacking.append(closestSerial) #If we did, append it to currentlyAttacking and return it (as a serial)
    return closestSerial

def nearbyPriorityCheck(): # This will check to see if we have a priority honor target in range and return it if so.
    if not priorityTargetList:
        return False
    nearbyEnemies = findTargets(False, killUnicorns, 12)
    if not nearbyEnemies:
        return False
    for testEnemy in nearbyEnemies:
        for testName in priorityTargetListLower:
            if testName in testEnemy.Name.lower():
                return testEnemy.Serial
            continue
        continue
    return False

# This is the function that uses the target finding above to aggro everything in the relevant range.
def getAggro():
    if not aggroMobs:
        return False
    attackSerial = None
    honorSerial = None
    aggroSerial = None
    aggroSerial = findAggroSerial()
    if not aggroSerial:
        return False
    attackSerial = findAggroSerial(True)
    if not attackSerial or (sameTarget and not Player.BuffsExist("Perfection")):
        honorSerial = findAggroSerial(True, True)
        if honorSerial:
            honorTarget(honorSerial)
    Player.Attack(aggroSerial)
    Misc.Pause(100)
    return True

def attackEnemy():
    attackSerial = None
    honorSerial = None
    attackSerial = findAggroSerial(True)
    if not attackSerial:
        honorSerial = findAggroSerial(True, True)
        if honorSerial:
            honorTarget(honorSerial)
        eooPriorityCast()
        return False             
    if sameTarget and not Player.BuffsExist("Perfection"):
        honorSerial = findAggroSerial(True, True)
        if honorSerial:
            honorTarget(honorSerial)
    else:
        honorTarget(attackSerial)
    Player.Attack(attackSerial)
    Misc.Pause(100)
    eooPriorityCast()
    return True

def eooPriorityCast():
    if not eooPriorityTargets:
        return False
    badTargets = False
    targetsList = findTargets(False, killUnicorns, 8)
    if not targetsList and not Player.BuffsExist("Enemy of One"):
    #    Player.HeadMessage(65, "No targets, no buff")
        return False
    if not targetsList and Player.BuffsExist("Enemy of One"):
    #    Player.HeadMessage(65, "No targets, removing buff")
        Spells.CastChivalry("Enemy of One")
        Timer.Create("spellTimer", 1000)
        Misc.Pause(100)
        return False
    for testName in targetsList:
        foundPriorityTarget = False
        for priorityName in priorityTargetListLower:
            if priorityName in testName.Name.lower():
                foundPriorityTarget = True
                break
        if not foundPriorityTarget:
            badTargets = True
            break
    if badTargets and not Player.BuffsExist("Enemy of One"):
    #    Player.HeadMessage(65, "Bad targets, no buff")
        return False
    if badTargets and Player.BuffsExist("Enemy of One"):
    #    Player.HeadMessage(65, "No targets, removing buff")
        Spells.CastChivalry("Enemy of One")
        Timer.Create("spellTimer", 1000)
        Misc.Pause(100)
        return False
    if Player.BuffsExist("Enemy of One"):
    #    Player.HeadMessage(65, "Good target, but buffed")
        return True
    #Player.HeadMessage(65, "Good target, buffing")
    Spells.CastChivalry("Enemy of One")
    Timer.Create("spellTimer", 1000)
    Misc.Pause(100)
    return True


def honorTarget(honoreeSerial):
    if not honorTargets:
        return False
    if Timer.Check("honorTimer"):
        return False
    honorOverride = None
    if honorPriorityTargets:
        honorOverride = nearbyPriorityCheck()
    if honorOverride:
        honoreeSerial = honorOverride
    honoree = Mobiles.FindBySerial(honoreeSerial)
    if not honoree:
        return False
    if honoree.Hits != honoree.HitsMax or Player.DistanceTo(honoree) > 10:
        return False
    Player.InvokeVirtue("Honor")
    Target.WaitForTarget(1000)
    Journal.Clear()
    Target.TargetExecute(honoree)
    Misc.Pause(100)
    if Journal.Search("need to declare"):
        Timer.Create("honorTimer", 500)
    Target.Cancel()
    Misc.Pause(100)


def countNearby(nearRadius=1):
    closeEnemies = findTargets(False, killUnicorns, nearRadius)
    if not closeEnemies:
        return 0
    return len(closeEnemies)

def decurse():
    if not Player.BuffsExist('Blood Oath (curse)'):
        return False
    Spells.CastChivalry('Remove Curse')
    Target.WaitForTarget(2000)
    Target.Self()
    Misc.Pause(100)
    return True

def bushidoTraining():
    if Timer.Check("bushidoTimer"):
        return False
    if Player.GetSkillValue("Bushido") < 60:
        if Player.BuffsExist("Confidence"):
            return False
        Spells.CastBushido("Confidence")
        Timer.Create("bushidoTimer", 200)
    elif Player.GetSkillValue("Bushido") < 75:
        if Player.BuffsExist("Counter Attack"):
            return False
        Spells.CastBushido("Counter Attack")
        Timer.Create("bushidoTimer", 200)
    elif Player.GetSkillValue("Bushido") < 97:
        if Player.BuffsExist("Evasion"):
            return False
        Spells.CastBushido("Evasion")
        Timer.Create("bushidoTimer", 200)
    elif Player.GetSkillValue("Bushido") < 120:
        if Player.BuffsExist("Momentum Strike"):
            return False
        Spells.CastBushido("Momentum Strike")
        Timer.Create("bushidoTimer", 200)
    Misc.Pause(100)
    return True
 
def ChooseAbility():
    if (Player.DistanceTo(currentTargetSerial) <= 1):
        weapon = Player.GetItemOnLayer(meleehand)
        meleeranged = 'melee'
        if not weapon:
            Dress.ChangeList(meleedress1)
            Misc.Pause(50)
            Dress.DressFStart()
            Misc.Pause(600)
            weapon = Player.GetItemOnLayer(meleehand)
        elif weapon.Serial == rangedserial:
            Dress.ChangeList(meleedress1)
            Misc.Pause(50)
            Dress.DressFStart()
            Misc.Pause(600)
            weapon = Player.GetItemOnLayer(meleehand)
        elif not weapon:
            Misc.Pause(250)
            ChooseAbility()
    if (Player.DistanceTo(currentTargetSerial) >= 2):
        weapon = Player.GetItemOnLayer(rangedhand)
        meleeranged = 'ranged'
        if not weapon:
            Dress.ChangeList(rangeddress)
            Misc.Pause(50)
            Dress.DressFStart()
            Misc.Pause(600)
            weapon = Player.GetItemOnLayer(rangedhand)
        elif weapon.Serial == meleeserial1:
            Dress.ChangeList(rangeddress)
            Misc.Pause(50)
            Dress.DressFStart()
            Misc.Pause(600)
            weapon = Player.GetItemOnLayer(rangedhand)
        elif not weapon:
            Misc.Pause(250)
            ChooseAbility()            
    #Count enemies within 2 spaces
    cntEnemy = countNearby(2)
    #Choose which ability to use
    if meleecustom == True and meleeranged == 'melee':
        if cntEnemy > 1 and Player.Mana >= msmana and not custommeleePrimarySA == 'WW' and not custommeleeSecondarySA == 'WW' and not Player.BuffsExist('Momentum Strike'): 
            Spells.CastBushido('Momentum Strike')
            Misc.Pause(100)
        elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana and custommeleePrimarySA == 'WW':
            Player.WeaponPrimarySA() #frenzied whirlwind or whirlwind
            Misc.Pause(100)
        elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana and custommeleeSecondarySA == 'WW':
            Player.WeaponSecondarySA() #frenzied whirlwind or whirlwind
            Misc.Pause(100)
        elif cntEnemy == 1 and Player.Mana > lsmana and custommeleePrimarySA == 'NA' and custommeleeSecondarySA == 'NA' and not Player.BuffsExist('Lightning Strike'):
            Spells.CastBushido('Lightning Strike')
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedPrimarySA == 'DS':
            Player.WeaponPrimarySA() #double shot or double strike
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedSecondarySA == 'DS':
            Player.WeaponSecondarySA() #double shot or double strike
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedPrimarySA == 'SA':
            Player.WeaponPrimarySA() #bleed, ignore armor or infectious strike
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedSecondarySA == 'SA':
            Player.WeaponSecondarySA() #bleed, ignore armor or infectious strike
            Misc.Pause(100)
    elif rangedcustom == True and meleeranged == 'ranged':
        if cntEnemy > 1 and Player.Mana >= msmana and not customrangedPrimarySA == 'WW' and not customrangedSecondarySA == 'WW' and not Player.BuffsExist('Momentum Strike'): 
            Spells.CastBushido('Momentum Strike')
            Misc.Pause(100)
        elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana and customrangedPrimarySA == 'WW':
            Player.WeaponPrimarySA() #frenzied whirlwind or whirlwind
            Misc.Pause(100)
        elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana and customrangedSecondarySA == 'WW':
            Player.WeaponSecondarySA() #frenzied whirlwind or whirlwind
            Misc.Pause(100)
        elif cntEnemy == 1 and Player.Mana > lsmana and customrangedPrimarySA == 'NA' and customrangedSecondarySA == 'NA' and not Player.BuffsExist('Lightning Strike'):
            Spells.CastBushido('Lightning Strike')
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedPrimarySA == 'DS':
            Player.WeaponPrimarySA() #double shot or double strike
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedSecondarySA == 'DS':
            Player.WeaponSecondarySA() #double shot or double strike
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedPrimarySA == 'SA':
            Player.WeaponPrimarySA() #bleed, ignore armor or infectious strike
            Misc.Pause(100)
        elif cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana and customrangedSecondarySA == 'SA':
            Player.WeaponSecondarySA() #bleed, ignore armor or infectious strike
            Misc.Pause(100)
    else:
        if "war axe" in weapon.Name:
            # Choose ability: 2 = Momentum Strike, anything else, just Armor Ignore
            if cntEnemy > 1 and Player.Mana >= msmana and not Player.BuffsExist('Momentum Strike'): 
                Spells.CastBushido('Momentum Strike')
                Misc.Pause(100)
            elif Player.Mana >= aimana and not Player.HasSpecial:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)
            #if cntEnemy > 2:
                #Player.HeadMessage(0,"Swap to BLACK STAFF IDIOT!")
        elif "radiant scimitar" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and Player.Mana > lsmana and not Player.BuffsExist('Lightning Strike'):
                Spells.CastBushido('Lightning Strike')
                #Player.HeadMessage(0,"Swap to BLADED STAFF or HATCHET IDIOT!")
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponPrimarySA() #Whirlwind
                Misc.Pause(100)
        elif "black staff" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and not Player.BuffsExist('Lightning Strike'):
                Spells.CastBushido('Lightning Strike')
                #Player.HeadMessage(0,"Swap to WAR AXE IDIOT!")
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponPrimarySA() #Whirlwind
                Misc.Pause(100)
        elif "bladed staff" in weapon.Name:
            # Choose ability: 2 = Momentum Strike, anything else, just Armor Ignore
            if cntEnemy >= 2 and Player.Mana >= msmana and not Player.BuffsExist('Momentum Strike'): 
                Spells.CastBushido('Momentum Strike')
                Misc.Pause(100)
            elif Player.Mana >= aimana and not Player.HasSpecial:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)
            #if cntEnemy > 2:
                #Player.HeadMessage(0,"Swap to RADIANT SCIMITAR or DOUBLE AXE IDIOT!")
        elif "hatchet" in weapon.Name:
            # Choose ability: 2 = Momentum Strike, anything else, just Armor Ignore
            if cntEnemy >= 2 and Player.Mana >= msmana and not Player.BuffsExist('Momentum Strike'): 
                Spells.CastBushido('Momentum Strike')
                Misc.Pause(100)
            elif Player.Mana >= aimana and not Player.HasSpecial:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)
            #if cntEnemy > 2:
                #Player.HeadMessage(0,"Swap to RADIANT SCIMITAR or DOUBLE AXE IDIOT!")
        elif "double axe" in weapon.Name:
            # Choose ability: 1 = Double Strike, 2+ = Whirlwind
            if cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana:
                Player.WeaponPrimarySA() #DoubleStrike
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponSecondarySA() #Whirlwind
                Misc.Pause(100)
        elif "large battle axe" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana:
                Spells.CastBushido('Lightning Strike')
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponPrimarySA() #Whirlwind
                Misc.Pause(100)            
        elif "halberd" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana:
                Spells.CastBushido('Lightning Strike')
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponPrimarySA() #Whirlwind
                Misc.Pause(100)            
        elif "soul glaive" in weapon.Name:
            if not Player.HasSpecial and Player.Mana >= aimana:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)
        elif "composite bow" in weapon.Name:
            if not Player.HasSpecial and Player.Mana >= aimana:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)    
        elif "yumi" in weapon.Name:
            if not Player.HasSpecial and Player.Mana >= aimana:
                Player.WeaponSecondarySA() #Double Shot
                Misc.Pause(100)
        elif "throwing hatchet" in weapon.Name:
            if not Playeumir.HasSpecial and Player.Mana >= aimana:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)
        elif "throwing dagger" in weapon.Name:
            if not Player.HasSpecial and Player.Mana >= aimana:
                Player.WeaponSecondarySA() #Infectious Strike
                Misc.Pause(100) 
        elif "throwing clever" in weapon.Name:
            if not Player.HasSpecial and Player.Mana >= aimana:
                Player.WeaponPrimarySA() #Bleed Attack
                Misc.Pause(100)                     
        elif "war hammer" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and not Player.BuffsExist('Lightning Strike'):
                Spells.CastBushido('Lightning Strike')
                #Player.HeadMessage(0,"Swap to WAR AXE IDIOT!")
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponPrimarySA() #Whirlwind
                Misc.Pause(100) 
        elif "quarter staff" in weapon.Name:
            # Choose ability: 1 = Double Strike, 2+ = Whirlwind
            if cntEnemy == 1 and not Player.HasSpecial and Player.Mana >= dsmana:
                Player.WeaponPrimarySA() #DoubleStrike
                Misc.Pause(100)
        elif cntEnemy >= 2 and Player.Mana >= msmana and not Player.BuffsExist('Momentum Strike'): 
                Spells.CastBushido('Momentum Strike')
                Misc.Pause(100)
        elif "hammer pick" in weapon.Name:
            # Choose ability: 2 = Momentum Strike, anything else, just Armor Ignore
            if cntEnemy >= 2 and Player.Mana >= msmana and not Player.BuffsExist('Momentum Strike'): 
                Spells.CastBushido('Momentum Strike')
                Misc.Pause(100)
            elif Player.Mana >= aimana and not Player.HasSpecial:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)
        elif "Spiked Whip" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and Player.Mana > lsmana and not Player.BuffsExist('Lightning Strike'):
                Spells.CastBushido('Lightning Strike')
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponSecondarySA() #Whirlwind
                Misc.Pause(100)
        elif "Bladed Whip" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and Player.Mana > lsmana and not Player.BuffsExist('Lightning Strike'):
                Spells.CastBushido('Lightning Strike')
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponSecondarySA() #Whirlwind
                Misc.Pause(100)
        elif "Barbed Whip" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and Player.Mana > lsmana and not Player.BuffsExist('Lightning Strike'):
                Spells.CastBushido('Lightning Strike')
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponSecondarySA() #Whirlwind
                Misc.Pause(100)
        elif "Insane Blade" in weapon.Name:
            # Choose ability: 2 = Momentum Strike, anything else, just Armor Ignore
            if cntEnemy >= 2 and Player.Mana >= msmana and not Player.BuffsExist('Momentum Strike'): 
                Spells.CastBushido('Momentum Strike')
                Misc.Pause(100)
            elif Player.Mana >= aimana and not Player.HasSpecial:
                Player.WeaponSecondarySA() #Armor Ignore
                Misc.Pause(100)
        elif "lajatang" in weapon.Name:
            # Choose ability: 1 = Lightning Strike, 2+ = Whirlwind
            if cntEnemy == 1 and not Player.BuffsExist('Lightning Strike'):
                Spells.CastBushido('Lightning Strike')
                Misc.Pause(100)
            elif cntEnemy > 1 and not Player.HasSpecial and Player.Mana >= wwmana:
                Player.WeaponSecondarySA() #FrenziedWhirlwind
                Misc.Pause(100)
        elif "spear" in weapon.Name:
            # Choose ability: 2 = Momentum Strike, anything else, just Armor Ignore
            if cntEnemy >= 2 and Player.Mana >= msmana and not Player.BuffsExist('Momentum Strike'): 
                Spells.CastBushido('Momentum Strike')
                Misc.Pause(100)
            elif Player.Mana >= aimana and not Player.HasSpecial:
                Player.WeaponPrimarySA() #Armor Ignore
                Misc.Pause(100)


    #Timer.Create("weaponTimer", 600)
 
 
currentlyAttacking = []
currentTargetSerial = None
sameTarget = False
dontKillLower = [x.lower() for x in dontKillList]
summonsLower = [x.lower() for x in summonsToIgnore]
healersLower = [x.lower() for x in healersToIgnore]
unicornListLower = [x.lower() for x in unicornList]
priorityTargetListLower = [x.lower() for x in priorityTargetList]
mobileStringsLower = [x.lower() for x in mobileStrings]
Player.HeadMessage(65, "Starting Sampire AIO")
while Player.Connected:
    # If you're a ghost, just got into a holding pattern until you're not.
    if Player.IsGhost:
        Misc.Pause(1000)
        continue

    Misc.Pause(100)
    # Make sure you have your permanent buffs up.
    buffCheck()
    decurse()
    # Get aggro from enemies.
    getAggro()
    # Attack your target. Remainder of things happen if you're actually in combat.
    if attackEnemy():
        # Train bushido to cap if set to do so, overriding other bushido buffs.
        if trainBushido and Player.GetSkillValue("Bushido") < bushidoCap:
            bushidoTraining()         
        # Maintain all in-combat buffs.
        combatBuffs()
        Misc.Pause(250)
        #Pick which ability to use
        ChooseAbility()
    else:
        masteryBuffsOff()