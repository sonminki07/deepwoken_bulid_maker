# 📚 Deepwoken Wiki: Talents (탤런트 (전체))
> **총 항목 수**: 1043개 | **출처**: https://deepwoken.co/wiki/talent

---

### Against All Odds `[Common]`
- **설명**: For each combat tag you have on your character, increase your damage by 2% (max of 14%). | **요구조건**: `{'stats': {'Willpower': 65}}`

### Emergency Reserves `[Common]`
- **설명**: When you get hit below 20% health, gain 20% tempo immediately. | **요구조건**: `{'stats': {'Willpower': 80}}`
- **추가 정보**: 3 minute cooldown.

### Unswayed `[Common]`
- **설명**: The effects of Taunt and Encore no longer work on you. | **요구조건**: `{'stats': {'Willpower': 75}}`
- **추가 정보**: The Taunt Mantra and Cornered Fool no longer work on you. Sing will still Charm you.

### Kick Off `[Common]`
- **설명**: You easily brush off shorter falls, taking no damage. Your first wall jump will always send you higher than normal. Gain a speed boost after wall jumping over a wall.  | **요구조건**: `{'stats': {'Agility': 20}}`
- **추가 정보**: Falls are considered to be 10 studs shorter, reducing fall damage. Climb height is increased by 15% with a 3s CD. Slide jumping further increases climb height.

### Steady Footing `[Common]`
- **설명**: You're much more resistant to being pushed around. | **요구조건**: `{'stats': {'Strength': 10, 'Agility': 10}}`
- **추가 정보**: Knockback is reduced by 20%. Ice's slide distance effect is removed.

### Time To Go `[Common]`
- **설명**: Taking a life grants a speed boost for 10 seconds. Taking a player's life doubles the speed boost and the duration. | **요구조건**: `{'stats': {'Agility': 5}}`

### An Ironsinger's Instinct `[Rare]`
- **설명**: Successfully dodging an attack coats you in metal and reduces the damage of the next attack taken. | **요구조건**: `{'stats': {'Ironsing': 75}}`
- **추가 정보**: Grants 60% damage reduction for 2 seconds. Ends early if you take damage. 18 second cooldown.

### Exposed Durability `[Common]`
- **설명**: Deal 10% more damage to opponents with no armor durability left. | **요구조건**: `{'stats': {'Ironsing': 60}}`
- **추가 정보**: Procs against Berserk users and while Berserk is active.

### Phantom Edge `[Rare]`
- **설명**: Your weapon M1's have +0.25 range. | **요구조건**: `{'stats': {'Ironsing': 75}}`

### Everchanging Aegis `[Rare]`
- **설명**: You take 20% less from attacks the same element as the last element you were hit with, but 10% more damage from attacks from different element. | **요구조건**: `{'stats': {'Intelligence': 25}}`
- **추가 정보**: Your Aegis type can swap on block, dodge, and parry.

### Neural Overload `[Advanced]`
- **설명**: You can input up to 4 copies of each Mantra ingredient instead of being limited to 3. | **요구조건**: `{'stats': {'Intelligence': 85}}`

### Overflowing Dam `[Rare]`
- **설명**: Having full Ether for 2 seconds or more grants an aura to your attacks that grant them 10% more damage. | **요구조건**: `{'stats': {'Intelligence': 40}}`
- **추가 정보**: For every point of Intelligence below 40, Overflowing Dam's damage bonus will be reduced by 0.125%, having a minimum damage buff of 6.875% at 15 Intelligence.

### Perfect Flash `[Rare]`
- **설명**: Having over 95% health causes your mantras to do +25% damage. This damage bonus will scale down to 10% if your enemies are far away. | **요구조건**: `{'stats': {'Intelligence': 25}}`

### Wyvern's Claw `[Rare]`
- **설명**: You deal 10% more damage while airborne. Mantras receive a 5% damage increase instead. | **요구조건**: `{'stats': {'Weapon': 25, 'Strength': 15}}`
- **추가 정보**: Activates after not being in contact with a grounded surface for ~0.75 seconds.

### Aerogliding `[Rare]`
- **설명**: When falling from a high place, hold spacebar to generate wind currents until you hit the floor. Also gives you more airtime with Gliders. | **요구조건**: `{'stats': {'Galebreathe': 35, 'Agility': 30}}`
- **추가 정보**: When active, create an aura that reduces fall speed and stops fall damage. Automatically ends after 5 seconds. The altitude loss while gliding is significantly reduced. This effect stacks with Tiran's Feathered Glider.

### Gale Trap `[Common]`
- **설명**: Knocking a player places a wind trap, causing anyone to pick up that body to get sent flying. Gain a speed boost picking up the body yourself. Killing PvE opponents gives you Gale Reflection instead. | **요구조건**: `{'stats': {'Galebreathe': 50}, 'talents': ['Wind Step']}`
- **추가 정보**: Marks players knocked by you for 6s with "Gale Trap". If the user picks up a target they've marked, they will gain a 35% speed boost for 20 seconds. But if anyone else attempts to pick up the marked target, they will be ragdolled and flung upwards. This includes the user's allies. Gale Reflection activates upon getting hit by an enemy, granting damage reduction to the attack and placing a Gale Trap on them. The damage of the Gale Trap scales with the strength of the enemy you killed.

### Suffocating Impact `[Common]`
- **설명**: When flourishing enemies into walls they are suffocated and winded for a short duration. | **요구조건**: `{'stats': {'Strength': 15, 'Galebreathe': 35}}`

### Stifled Jump `[Rare]`
- **설명**: Suffocating now applies Dazed if enemies jump. Suffocated PvE enemies now also get Sluggish when they are suffocated. | **요구조건**: `{'talents': ['Suffocating Impact']}`
- **추가 정보**: The daze effect lasts for 1 second.

### Apothecary `[Common]`
- **설명**: Potions you prepare will have amplified positive effects when consumed, and amplified negative effects when thrown. | **요구조건**: `{'stats': {'Intelligence': 10}, 'objectives': ['Interact with a cauldron']}`
- **추가 정보**: Additively increases potion Potency by 125%. Acts similarly to a potion ingredient, remaining active if you no longer have the Talent.

### Chain Reaction `[Common]`
- **설명**: When applying a potion effect to someone who already has one, the new effect is amplified. You have a 25% chance not to deplete potions when drinking them. | **요구조건**: `{'stats': {'Intelligence': 80}, 'objectives': ['Interact with a cauldron']}`
- **추가 정보**: Procs when a thrown potion replaces a different potion's effect, increasing your potion's effect by 40% multiplicatively.

### Placebo Effect `[Rare]`
- **설명**: Drinking potions near allies will share the potion's effect with them. | **요구조건**: `{'stats': {'Intelligence': 60}, 'objectives': ['Interact with a cauldron']}`
- **추가 정보**: Also procs potion sickness, causing allies to throw up upon usage if they've ingested a potion recently.

### Potion Quaffer `[Rare]`
- **설명**: You're accustomed to drinking toxic fluids quickly. You'll get along famously with the other patrons at the tavern. Drinking potions slows less and grants superior regenerative effects to you. | **요구조건**: `{'stats': {'Intelligence': 30}, 'objectives': ['Interact with a cauldron'], 'or': [{'stats': {'Fortitude': 15}}, {'stats': {'Willpower': 15}}]}`
- **추가 정보**: Drink potions 30% faster. Increases the effectiveness of Health Regeneration potions by 15%, Sanity Restoration and Ether Regeneration potions by 30%, and removes the -25% effectiveness Instant Health potions have.

### Endurance Runner `[Common]`
- **설명**: Your speed is decreased less by low health. | **요구조건**: `{'stats': {'Agility': 25, 'Fortitude': 25}}`

### Scaredy Cat `[Common]`
- **설명**: When enemies initiate a fight first, gain a speed boost. | **요구조건**: `{'stats': {'Agility': 5}}`

### Conditioned Runner `[Advanced]`
- **설명**: You regenerate health faster than normal when sprinting below 75% HP. The health amount scales with your agility stat. | **요구조건**: `{'stats': {'Agility': 25}, 'talents': ['Endurance Runner', 'Scaredy Cat']}`
- **추가 정보**: After 3 seconds of sprinting without taking damage, gain increased health regeneration.  The increased health regeneration is equal to +(Agility × 2)% health regen, having no bonus at 0 Agility, and scaling up to +200% at 100 Agility. This Talent is disabled in Chime of Conflict.

### Approaching Singularity `[Common]`
- **설명**: You now gain +1% Mantra PEN for every 10 point of Intelligence. | **요구조건**: `{'stats': {'Intelligence': 80}}`
- **추가 정보**: Gives 0.1% Mantra PEN per point in Intelligence.

### Flame Within `[Common]`
- **설명**: An application of Pleeksty's concept of the inner flame, also known as the soul of man. Set yourself ablaze to gain more move speed and 10% extra damage. | **요구조건**: `{'stats': {'Flamecharm': 25}}`
- **추가 정보**: 8 second cooldown on cast. The self burn can only be dispelled by using the tool again or through the rain/sea.

### Proficient Baiting `[Quest]`
- **설명**: Casting your line excites ocean life, reducing the chances of fishing up trash. | **요구조건**: `{'quests': ['Fish 10 times']}`
- **추가 정보**: Reduces the likelihood of fishing up trash items such as Seaweed or Leather Boots.

### Hook, Line, and Sinker `[Quest]`
- **설명**: Once something's caught your line, it's much harder to get loose. | **요구조건**: `{'quests': ['Fish 30 times']}`
- **추가 정보**: Slightly increases margin of failure before losing a fish.

### Fisher's Lure `[Quest]`
- **설명**: Fish are drawn to your line more quickly. | **요구조건**: `{'quests': ['Fish 50 times']}`
- **추가 정보**: Slightly increases the chance of hooking something while fishing.

### Collapsed Lung `[Advanced]`
- **설명**: Block breaking an opponent closes off their ability to Vent for 8s, with this duration scaling with Strength. PvE enemies instead get Collapsed. | **요구조건**: `{'stats': {'Strength': 100}}`
- **추가 정보**: This effect lasts 8 seconds and loses 0.04s for every investment point below 100 Strength. The Collapsed status effect reduces the posture damage affected enemies deal to you by 40%.

### Carnivore `[Rare]`
- **설명**: In return for losing the ability to eat vegetation, satiate your hunger by killing others. | **요구조건**: `{'stats': {'Strength': 5, 'Willpower': 5}}`
- **추가 정보**: Cannot be obtained if you have the Vegetarian Flaw.

### Grand Feast `[Common]`
- **설명**: Regain tempo, ether, blood and health when gaining hunger from killing. | **요구조건**: `{'talents': ['Carnivore']}`
- **추가 정보**: Health gain is disabled in PvP combat. On proc, gain 40% tempo, 55% Ether, 3% blood, and 5% health.

### Sunken Predator `[Common]`
- **설명**: Enemies you hit in the water or the depths have their speed buffs nullified and are slowed. | **요구조건**: `{'stats': {'Power': 11}}`

### Oath: Arcwarder `[Oath]`
- **설명**: You vow to be a shield for your comrades, to wear your regalia with pride and serve the greater collective. From each according to their ability, to each according to their needs. | **요구조건**: `{'stats': {'Fortitude': 20, 'Flamecharm': 20, 'Thundercall': 20}, 'quests': ['Alpha']}`

### Arc Module: Dash `[Oath]`
- **설명**: [In Arc Suit] Your dashes become Jet Dashes, allowing you to attack while dashing. | **요구조건**: `{'talents': ['Oath: Arcwarder']}`
- **추가 정보**: Jet dashes go much further than regular dashes. Also allows the user to M1 while performing a dash, ending their dash early.

### Arc Module: Eject `[Oath]`
- **설명**: [In Arc Suit] When blockbroken, eject from your suit. | **요구조건**: `{'talents': ['Oath: Arcwarder'], 'or': [{'slay': 'Chaser or Ethiron'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Your posture will be set to 50% on activation.

### Arc Module: Enhance `[Oath]`
- **설명**: [In Arc Suit] Your Arcwarder Mantras deal increased damage. | **요구조건**: `{'talents': ['Oath: Arcwarder'], 'or': [{'slay': 'Chaser or Ethiron'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Arc Beam's base dmg is increased by 50%, Arc Wave's base damage is increased by 25%.

### Arc Module: Guard `[Oath]`
- **설명**: [In Arc Suit] You can block attacks from any direction and cannot be backstabbed. | **요구조건**: `{'talents': ['Oath: Arcwarder'], 'or': [{'slay': 'Chaser or Ethiron'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Prevents "backhit" Talents from proccing and grants 360 block against all attacks.

### Arc Module: Leap `[Oath]`
- **설명**: [In Arc Suit] Holding Spacebar after double jumping propels you up for a short duration. | **요구조건**: `{'talents': ['Oath: Arcwarder'], 'or': [{'slay': 'Chaser or Ethiron'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: 10 second CD outside of combat, 15 second CD in combat.

### Arc Module: Null `[Oath]`
- **설명**: [In Arc Suit] Outgoing and incoming enchant effects are nullified. Can be toggled with N. | **요구조건**: `{'talents': ['Oath: Arcwarder'], 'or': [{'slay': 'Chaser or Ethiron'}, {'objectives': ['Pay 10 Knowledge']}]}`

### Master Craftsman `[Common]`
- **설명**: Your skills alone substitute the need for a Craft Station. | **요구조건**: `{'stats': {'Intelligence': 45}}`
- **추가 정보**: You can craft items that normally require a Crafting Station from your inventory.

### Deep Wound `[Common]`
- **설명**: Assassinating a target applies anti-heal for 20s and gives you a speed boost for 6s. Assassination damage now scales with level against mobs. | **요구조건**: `{'stats': {'Agility': 35}}`
- **추가 정보**: Applies 30% anti-heal.

### Lights Out `[Common]`
- **설명**: Assassinations now give you 30% PEN and blind the target for 5s. Those you carry are now blindfolded. | **요구조건**: `{'stats': {'Agility': 55}}`

### Lowstride `[Common]`
- **설명**: When crouching, your stealth and roll distance are increased. Your speed while crouching is less slow. You now draw your weapon silently. | **요구조건**: `{'stats': {'Agility': 20}}`
- **추가 정보**: Doubles the stealth bonuses from crouching; stealth × 1.5 + 50 -> stealth × 2 + 100. Also silences the sheathe sound effect.

### Unseen Threat `[Common]`
- **설명**: You can assassinate those with weapons out provided you're not in combat yourself. Those you assassinate are slowed and unable to jump for 3s. | **요구조건**: `{'stats': {'Agility': 60}, 'talents': ['Deep Wound']}`

### Authority Intimidation `[Common]`
- **설명**: Lightning moves slow your opponent more. | **요구조건**: `{'stats': {'Power': 10, 'Thundercall': 60}}`

### Resolve Crusher `[Common]`
- **설명**: Lightning moves now apply stacks of 'Resolve Crusher'. At 4 stacks, you apply 'Electrified' to your opponent. Attacks from Electrified opponents are converted into lightning damage, but will deal 10% less damage to you. | **요구조건**: `{'stats': {'Thundercall': 65}}`
- **추가 정보**: Resolve Crusher's "Electrified" effect is only applied after the 5th stack (not the 4th stated by the Talent). Each stack lasts for 5 seconds. Electrified lasts for 5 seconds. Damage debuff only applies against weapon attacks.

### First Interrogation `[Common]`
- **설명**: Attacks from opponents who are Electrified will give you ether proportional to their initial damage. | **요구조건**: `{'stats': {'Thundercall': 65}, 'talents': ['Resolve Crusher']}`
- **추가 정보**: Only procs on weapon attacks from Electrified opponents. Ether given is half of their scaled damage.

### Second Interrogation `[Common]`
- **설명**: Attacks from Electrified opponents deal 50% less damage and 50% less posture damage to you. | **요구조건**: `{'stats': {'Thundercall': 65}, 'talents': ['First Interrogation']}`
- **추가 정보**: Does not stack with Resolve Crusher's damage reduction, instead it replaces it with this, more potent, effect. Only applies against weapon attacks.

### Horn of Authority `[Origin]`
- **설명**: Mark escaping prisoners. | **요구조건**: `{'origin': 'Authority Ensign'}`

### Authority Ensign `[Origin]`
- **설명**: You are a member of the Authority deployed to the Eastern Luminant. You may find trouble with the local factions and must become stronger through advancing the Authority's position. | **요구조건**: `{'origin': 'Authority Ensign'}`

### Battle Tendency `[Common]`
- **설명**: You can breathe more easily with +20% faster posture regen. | **요구조건**: `{'stats': {'Fortitude': 15, 'Willpower': 15}}`
- **추가 정보**: This only affects passive posture regeneration.

### Braced Collapse `[Common]`
- **설명**: After being block broken, the next attack to hit you deals reduced damage. | **요구조건**: `{'stats': {'Fortitude': 25}}`
- **추가 정보**: After being block broken, reduce the next instance of damage by 20%. This has no cooldown.

### Moving Fortress `[Common]`
- **설명**: Blocking no longer slows you down as much. | **요구조건**: `{'stats': {'Fortitude': 5}}`
- **추가 정보**: Increases your movement speed while blocking by 5%, from -25% movement speed to -20%.

### Perseverance `[Common]`
- **설명**: Reduces the duration you're Ragdolled and Unconscious for by 25%. | **요구조건**: `{'stats': {'Fortitude': 30, 'Willpower': 30}}`
- **추가 정보**: This can stack with other Talents to reduce knock time even further. (Ex. Defiance)

### Reinforced Armor `[Advanced]`
- **설명**: Incoming PEN is reduced by 30%. | **요구조건**: `{'stats': {'Fortitude': 90}, 'talents': ['Battle Tendency', 'Braced Collapse', 'Moving Fortress', 'Perseverance']}`
- **추가 정보**: Loses 0.8% PEN resistance per point below 90 Fortitude, capping at 10% PEN resistance at 65 Fortitude.

### Armored Plating `[Faction]`
- **설명**: Put on extra plating on your armor, giving you 50 temp health whenever you are put in combat. Due to the weight of this additional plating, you have reduced speed at all times. | **요구조건**: `{'origin': 'Authority Ensign'}`

### Crossguard `[Faction]`
- **설명**: If you are using a sword, you gain 10% chip against other opponents wielding swords. | **요구조건**: `{'origin': 'Authority Ensign'}`
- **추가 정보**: This is additive to weapon chip damage.

### Riot Shield `[Faction]`
- **설명**: While you are fighting two or more opponents and are using a shield, reduce the total amount of chip damage you take by 40%. | **요구조건**: `{'origin': 'Authority Ensign'}`
- **추가 정보**: Grants 40% damage reduction to chip damage, does not reduce your opponent's chip % by 40.

### Oppressive Force `[Faction]`
- **설명**: When using a weapon found in the Merit Armory, gain a unique two-hit flourish that does not knock back opponents and dazes them. | **요구조건**: `{'origin': 'Authority Ensign'}`
- **추가 정보**: The first hit deals your regular M1 damage and posture damage, the second hit deals 80% of your weapon's scaled damage with 7 posture damage. The damage and posture damage of the second hit cannot be buffed. The second hit does not count as a weapon attack, and therefore it does not benefit from any of your weapon's stats and cannot proc Talent effects.

### Steel Tread `[Faction]`
- **설명**: Gain a bit of knockback resistance as well as damage resistance against attacks that ragdoll you. | **요구조건**: `{'origin': 'Authority Ensign'}`

### Oath: Blindseer `[Oath]`
- **설명**: You vow to not let the horrors of the world pierce your tightly fastened blindfold. Everything is simply as we choose to perceive it. | **요구조건**: `{'stats': {'Willpower': 40}, 'talents': ['Breathing Exercise', 'Conquer your Fears', 'Disbelief']}`
- **추가 정보**: You can now see while blinded, but the world gains a blue hue.

### All-Seeing Eye `[Oath]`
- **설명**: The mystic eye through which you now see the world can perceive the imperceptible. Invisible foes are highlighted. | **요구조건**: `{'talents': ['Oath: Blindseer'], 'or': [{'quests': ['Help 4 Pathfinders escape the Depths']}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Invisible players, including yourself, and monsters are revealed by a Blindseer Eye icon showcasing their current position.

### Berserk `[Common]`
- **설명**: One with nothing to lose has everything to gain. Succumb to burning rage within and enter Berserk State. | **요구조건**: `{'stats': {'Strength': 80}}`
- **추가 정보**: Grants a Talent tool that, while active, turns all incoming damage into true damage, but gives you increased melee PEN. You gain increased PEN on your light attacks, scaling on how low your health is, and +10% PEN on your critical attacks. The PEN gained on light attacks in PvP does not bypass the PEN cap, and requires Million Ton Piercer to go over +50%. In PvE, gain +100% PEN on your M1s instead. Lasts 20 seconds, halved to 10 if you do not meet the Talent requirements.

### Oath: Bladeharper `[Oath]`
- **설명**: You vow to carry your blades as an instrument, to lend yourself to any cause it guides you to. Collapse the infinite number of possibilities ahead of you into just one. The blade keeps you as much as you keep it.  | **요구조건**: `{'add': [{'stats': ['Light Weapon', 'Medium Weapon', 'Heavy Weapon'], 'value': 90}], 'or': [{'stats': {'Agility': 25}}, {'stats': {'Strength': 25}}, {'stats': {'Medium Weapon': 75}}]}`

### Float Like a Butterfly `[Oath]`
- **설명**: While having True Strength active, cancel your air dash to enter a frenzy of slashes. | **요구조건**: `{'talents': ['Oath: Bladeharper'], 'slay': 'Mind Reflection 3 times'}`
- **추가 정보**: 5s CD. Only accessible if True Strength is active. Deals 24 Oath + Slash damage (4 hits that deal 7 damage each).

### Lithe Step `[Oath]`
- **설명**: When Sprinting, roll-cancel and instantly vanish and surge with unmatched speed. | **요구조건**: `{'talents': ['Oath: Bladeharper']}`
- **추가 정보**: Provides a brief speed boost on proc. 3s CD, reduced to 1s if in True Strength.

### Reveal `[Oath]`
- **설명**: Pour your heart out, and reveal your true strength. | **요구조건**: `{'talents': ['Oath: Bladeharper'], 'slay': 'Mind Reflection 3 times'}`
- **추가 정보**: Grants a Talent tool that activates True Strength on use. While active, you will passively accumulate Wither. Reveal will automatically end if your health goes below 10%.

### Soaring Storm `[Oath]`
- **설명**: Empower your uppercuts with the way of the blade, after Lithe Stepping, flourishing, or landing an Oath ability. | **요구조건**: `{'talents': ['Oath: Bladeharper'], 'slay': 'Mind Reflection 2 times'}`
- **추가 정보**: Proc condition is removed and damage is increased if in True Strength. Applies to all forms of uppercuts, including Mantras and certain weapon criticals. Deals 24 Oath + Slash damage (6 hits that deal 4 damage each), this is increased to 39 damage (6 hits that deal 6.5 damage each) if you are in True Strength.

### Untouchable `[Oath]`
- **설명**: By landing consecutive hits on your opponent without taking any damage, reveal your True Strength for a short duration. | **요구조건**: `{'talents': ['Oath: Bladeharper'], 'slay': 'Mind Reflection 2 times'}`
- **추가 정보**: Grants True Strength for 15 seconds on proc. Untouchable requires 10 'Untouchable Stacks'. Being hit by any non-self damage source will reset all Untouchable Stacks. Weapon attacks give 2 stacks each, and non-weapon attacks give 1 stack each.

### Oath: Blightsurger `[Oath]`
- **설명**: Fists and storm. Wield sacred lightning, tear through foes and leave them withered. | **요구조건**: `{'add': [{'stats': ['Strength', 'Fortitude', 'Agility'], 'value': 80}, {'stats': ['Galebreathe', 'Thundercall'], 'value': 40}]}`

### Anchor Shock `[Oath]`
- **설명**: Your Blightshock prevents targets from using mobility mantras. | **요구조건**: `{'talents': ['Oath: Blightsurger'], 'objectives': ['Use Sovereign State while in combat 67 times']}`
- **추가 정보**: This puts your opponent's mobility slot Mantras on a 3 second cooldown whenever Blightshock is applied from a Blightsurger Mantra.

### Blight Pierce `[Oath]`
- **설명**: Your Blightshock attacks pierce through your enemies hyperarmor and gain more penetration. | **요구조건**: `{'talents': ['Oath: Blightsurger'], 'objectives': ['Use Sovereign State while in combat 37 times']}`
- **추가 정보**: Blightshock now works similar to regular Shock, canceling hyperarmor.

### Blighted Touch `[Oath]`
- **설명**: Landing Basic Attacks during Sovereign State now applies Blightshock. | **요구조건**: `{'talents': ['Oath: Blightsurger'], 'objectives': ['Use Sovereign State while in combat 22 times']}`
- **추가 정보**: This allows your Sovereign Bangle to apply Wither on hit.

### Blightlash `[Oath]`
- **설명**: Your swing range is enhanced during Sovereign State. | **요구조건**: `{'talents': ['Oath: Blightsurger'], 'objectives': ['Use Sovereign State while in combat 82 times']}`
- **추가 정보**: Increases the range of the Sovereign Bangle from 6 to 7.

### Sovereign State `[Oath]`
- **설명**: Landing physical hits builds your Blight Meter. At full gauge, enter a Blight State that changes your critical and empowers Blightsurge abilities. | **요구조건**: `{'talents': ['Oath: Blightsurger']}`
- **추가 정보**: Landing Galebreathe Mantras, Thundercall Mantras, weapon attacks, and Blightsurger Mantras gives Blight Meter. Press [X] while having at least 30% Blight Meter to enter the Sovereign State. Your weapon is replaced with Sovereign Bangle and the Wither applied on Blightsurger Mantras is increased while in Sovereign State.

### Bloodwarden's Sense `[Common]`
- **설명**: Enemies you attack with a mantra above 60% Blood Poisoning are marked with Bloodwarden's Mark for 5s. | **요구조건**: `{'stats': {'Bloodrend': 30}}`
- **추가 정보**: Adds a red highlight to the player and makes them take 20% more Blood Poisoning.

### Smell of Blood `[Rare]`
- **설명**: Enemies that touch your blood pools or are blockbroken by you are afflicted with Bloodscent for 6s. | **요구조건**: `{'stats': {'Bloodrend': 65}}`
- **추가 정보**: Your opponent's blood (or blood hemorrhaging in PvE) percentage is shown as a red number, and their blood poison percentage is shown as a pink number next to their character on proc.

### Bloodrend Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Bloodrend to its fullest. | **요구조건**: `{'stats': {'Bloodrend': 75}, 'talents': ['Master Bloodrender'], 'slay': 'Any humanoid boss'}`
- **추가 정보**: Removes the 75 investment cap on the Bloodrend Attribute. This Talent will be removed if you do not meet its stat requirements.

### Bloodrender `[Common]`
- **설명**: Grants you the ability to command Blood as a Bloodrender. Your Bloodrend mantras replenish your blood, steal blood and apply 'Blood Poisoning'. | **요구조건**: `{'stats': {'Bloodrend': 1}}`

### Adept Bloodrender `[Common]`
- **설명**: You can now obtain 1-star Bloodrender mantras. | **요구조건**: `{'stats': {'Bloodrend': 20}, 'talents': ['Bloodrender']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Expert Bloodrender `[Common]`
- **설명**: You can now obtain 2-star Bloodrender mantras. | **요구조건**: `{'stats': {'Bloodrend': 30}, 'talents': ['Adept Bloodrender']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Master Bloodrender `[Common]`
- **설명**: You can now obtain 3-star Bloodrender mantras. Your maximum blood capacity is 25% more than a normal individual. You regen blood at a quicker pace. | **요구조건**: `{'stats': {'Bloodrend': 50}, 'talents': ['Expert Bloodrender']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Crimson Fountain `[Common]`
- **설명**: Blockbreaking or flourishing an enemy now spills a pool of blood below them. Blood mantras cast within blood pools have a reduced blood cost. | **요구조건**: `{'stats': {'Bloodrend': 35}}`

### First Blood `[Common]`
- **설명**: Your first blood mantra you use in combat has no blood cost and deals additional blood drain . | **요구조건**: `{'stats': {'Bloodrend': 10}}`

### Hemorrhaging Blow `[Rare]`
- **설명**: Block breaking your opponent with a blood mantra turns your opponent's combat healing into damage for 8 seconds. | **요구조건**: `{'stats': {'Bloodrend': 95}, 'talents': ['Master Bloodrender']}`
- **추가 정보**: The damage to healing conversion is 1:1, meaning 20 healing = 20 damage. Works on all non-passive healing. 55 second cooldown, starting once the guardbreak occurs.

### Rush Hour `[Rare]`
- **설명**: Stab yourself to become stronger, faster, and deal increased blood bar damage. | **요구조건**: `{'stats': {'Bloodrend': 50}}`
- **추가 정보**: Use the Rush Hour tool to gain the Rush Hour status effect, granting a 30% speed boost, a 15% damage buff, and an increase to blood damage. This passively drains the user's health and blood while active. Recover 5% blood whenever you land an attack.

### Sanguine Siphon `[Common]`
- **설명**: Landing a critical attack while in a blood pool will consume that pool and empower your next blood mantra. | **요구조건**: `{'stats': {'Bloodrend': 40}}`
- **추가 정보**: Grants a 20% damage buff to the next Mantra cast.

### Blood and Iron `[Common]`
- **설명**: Pulling rods out of your opponent now replenishes an equivalent amount of blood. | **요구조건**: `{'stats': {'Bloodrend': 40, 'Ironsing': 40}}`

### Brain Death `[Common]`
- **설명**: Enemies that are already suffocated will have their suffocation duration extended when hit by a bloodrend mantra. | **요구조건**: `{'stats': {'Bloodrend': 40, 'Galebreathe': 40}}`
- **추가 정보**: Applies a new stack of suffocation on proc.

### Cold Blooded `[Common]`
- **설명**: Chilled enemies passively build up blood poison, alternatively when crystals explode it'll apply blood poison. (DOES NOT STACK) | **요구조건**: `{'stats': {'Bloodrend': 40, 'Frostdraw': 40}}`
- **추가 정보**: Applies 12.5% blood poisoning over the duration of the chill or 25% blood poisoning on crystal explosion. Only crystal explosions applied through maximizing crystal stacks will proc this Talent.

### Electrolyte `[Common]`
- **설명**: Hitting Bloodrend mantras while having temporary health applies Shocked while removing a portion of temporary health. | **요구조건**: `{'stats': {'Bloodrend': 40, 'Thundercall': 40}}`
- **추가 정보**: Applies a Surge Rod instead if you have Surge Path. Consumes 4 Temporary Health on proc.

### Malevolent Sapper `[Common]`
- **설명**: The more blood poisoning your opponent has, the more ether your shadow mantras steal from your opponent. | **요구조건**: `{'stats': {'Bloodrend': 40, 'Shadowcast': 40}}`

### Bruiser's Mixup `[Common]`
- **설명**: Switching your Fist Style mid-fight makes your basic Fist attacks inflict bleed temporarily. | **요구조건**: `{'weaponType': 'Fists'}`
- **추가 정보**: Lasts for 4 seconds.

### Impairing Blow `[Common]`
- **설명**: [Greataxes] Basic Attacks will slightly slow your enemy for 2 seconds. Running attacks will slow your enemy for 3 seconds. Gain +20% posture damage against enemies with speed boosts. | **요구조건**: `{'stats': {'Heavy Weapon': 30}, 'weaponType': 'Greataxe'}`
- **추가 정보**: Does not proc on uppercut.

### Brazen Blow `[Common]`
- **설명**: [Greataxes] Attacking an enemy slowed by your Greataxe grants you temporary hyperarmor. | **요구조건**: `{'stats': {'Heavy Weapon': 30}, 'weaponType': 'Greataxe'}`
- **추가 정보**: Only procs on weapon attacks. Does not proc on uppercut. 20 second cooldown.

### Heavy Fatigue `[Rare]`
- **설명**: [Greataxes] Hitting an enemy slowed by your Greataxe temporarily reduces how far they can roll and applies Sluggish to PvE enemies for a few seconds. | **요구조건**: `{'stats': {'Heavy Weapon': 40}, 'weaponType': 'Greataxe'}`
- **추가 정보**: Does not proc on uppercut.

### Rending Impact `[Rare]`
- **설명**: [Greataxes] Block breaking an enemy applies knockdown. | **요구조건**: `{'stats': {'Heavy Weapon': 40}, 'weaponType': 'Greataxe'}`
- **추가 정보**: Only procs on guardbreaks from weapon attacks. Applies knockdown for 1.2s.

### Defensive Reprisal `[Common]`
- **설명**: Being flourished grants you 10% posture resistance for 20s. | **요구조건**: `{'stats': {'Fortitude': 65}}`
- **추가 정보**: Defensive Reprisal's duration will be reduced by 0.177s for every point in Fortitude below its requirements, having a minimum duration of 15.55s duration with 40 Fortitude.

### Dancing Guard `[Common]`
- **설명**: Parrying an opponent and then parrying another enemy in quick succession applies slow for 7s. | **요구조건**: `{'stats': {'Fortitude': 55}}`
- **추가 정보**: Dancing Guard's duration will be reduced by 0.086s for every point in Fortitude below its requirements, having a minimum duration of 4.86s at 30 Fortitude.

### Down to your Level `[Common]`
- **설명**: While you have a speed debuff, your Basic Attacks slow your enemies for 5s. | **요구조건**: `{'stats': {'Fortitude': 60}}`
- **추가 정보**: Down to your Level's duration will be reduced by 0.05s for every point in Fortitude below 60, capping at a minimum of 3.75s with 35 Fortitude. The slow only procs on M1s or critical attacks with the M1 tag. Procs from Entanglement, Daze, Chill and most other things that slow you down.

### Knuckle Guard `[Common]`
- **설명**: Hitting Dazed enemies grants you 10% posture resistance for 15s. | **요구조건**: `{'stats': {'Fortitude': 55, 'Strength': 25}}`
- **추가 정보**: Knuckle Guard's duration will be reduced by 0.1s for every point of Fortitude and Strength below its requirements, having a minimum possible duration of 10.4 seconds with 30 Fortitude and 4 Strength.

### Swift Rebound `[Common]`
- **설명**: Move faster after successfully dodging an attack. | **요구조건**: `{'stats': {'Agility': 15}}`

### Evasive Expert `[Rare]`
- **설명**: Your speed boost granted from dodging is increased. | **요구조건**: `{'stats': {'Agility': 15}, 'talents': ['Swift Rebound']}`

### Risky Moves `[Rare]`
- **설명**: When you successfully dodge, you'll automatically dodge the next attack. | **요구조건**: `{'stats': {'Agility': 25}}`
- **추가 정보**: Attacking will cancel the effect early. 20 second cooldown.

### Ghost `[Advanced]`
- **설명**: Dodging a move will briefly make you invisible, ending early if you attack. | **요구조건**: `{'stats': {'Agility': 40}, 'talents': ['Swift Rebound', 'Evasive Expert', 'Risky Moves']}`
- **추가 정보**: The invisibility and I-frame duration is 1.2 seconds if you have 40 or higher Agility. Ghost's duration will be reduced by 0.0133 seconds per point in Agility under 40, capping at 0.866 seconds at 15 Agility. 20 second cooldown.

### Oath: Chainwarden `[Oath]`
- **설명**: You vow to be the chain that binds the wicked and drags them back where they belong. There are those in this world who should not be free. | **요구조건**: `{'add': [{'stats': ['Strength', 'Fortitude', 'Willpower'], 'value': 40}]}`

### Perpetual Wrath `[Oath]`
- **설명**: Unleash the true power of Restrain. Each successive hit will increase its damage. | **요구조건**: `{'talents': ['Oath: Chainwarden'], 'or': [{'slay': '1 Player with Hunted Authority reputation or Humanoid Boss'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Enchaining targets and hitting Chained targets with Restrain will add 1 stack of Perpetual Wrath. Each stack of Perpetual Wrath increases Restrain's (Mantra) damage by 8, capping out at 4 stacks for +32 damage.

### Chainlash `[Oath]`
- **설명**: On flourish, gain the ability to summon a chain on an enemy for 5 seconds by right clicking. This lets you whip your chain to seize and yank enemies towards you, setting them up for a crushing kick. | **요구조건**: `{'talents': ['Oath: Chainwarden'], 'or': [{'slay': '2 Players with Hunted Authority reputation or Humanoid Bosses'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Right clicking after a flourish will enchain your target and pull them towards you. M1ing after the pull will perform a Crushing Kick, dealing high damage.

### Champion's Regalia `[Rare]`
- **설명**: Flourishing an opponent grants you +50% posture damage on Basic Attacks for 10 seconds. | **요구조건**: `{'stats': {'Strength': 25}}`

### Defiance `[Rare]`
- **설명**: Negative status effects are half as effective when you are below 35% HP. | **요구조건**: `{'stats': {'Willpower': 70}}`
- **추가 정보**: The Effectiveness of Defiance will be lessened if you do not meet its Willpower requirement. Works on: Burn damage, the duration of Chill, Winded, Suffocation, time knocked, Ring of Pestilence, and Sightless Still, Crystal and Surge Rod gain, Blood Poisoning gain and Wither gain.

### Underdog `[Common]`
- **설명**: You deal 2.5% more damage to those with higher HP than you, scaling up to 4% at 60 WLL. Additionally, you deal +10% more damage to physically larger foes. | **요구조건**: `{'stats': {'Willpower': 30}}`
- **추가 정보**: Underdog grants a 2.5% damage buff at 20 Willpower, this is increased by 0.0375% damage per Willpower above 20, capping at 4% with 60 Willpower. Grants a 2.875% damage buff at requirements. "Higher HP" refers to current HP.

### Charismatic Cast `[Common]`
- **설명**: Landing a hit with a mantra on an enemy applies Charmed. Allies recover from being knocked twice as quickly when Charmed by you. | **요구조건**: `{'stats': {'Charisma': 25}}`
- **추가 정보**: Charismatic Cast's Charm lasts 10 seconds.

### Chaotic Charm `[Common]`
- **설명**: Charm enemies nearby when attacked at low health. Enemies affected by this charm have their damage increased to anyone but you, and deal reduced damage towards you. | **요구조건**: `{'stats': {'Charisma': 55}, 'talents': ['Charismatic Cast']}`
- **추가 정보**: Applies Chaotic Charm for 15 seconds, granting an additional source of damage reduction. Chaotic Charm gains 0.15% damage reduction for every point in Charisma you have.

### Lasting Charisma `[Common]`
- **설명**: Enemies charmed by your mantras are charmed longer. | **요구조건**: `{'stats': {'Charisma': 55}, 'talents': ['Charismatic Cast']}`
- **추가 정보**: This adds 10 seconds to Charismatic Charm's Charm duration, but this will be reduced by 0.16s for every point of Charisma below 55, capping at 15.8 seconds at 30 Charisma.

### Tough Love `[Common]`
- **설명**: Deal 10% more damage to enemies Charmed by you. Mantras deal +5% instead. Being hit by someone the same Aspect or Oath as you applies Charmed briefly. | **요구조건**: `{'stats': {'Charisma': 25}, 'talents': ['Charismatic Cast']}`
- **추가 정보**: Charms for 2 seconds with a 1 second cooldown. Tough Love's damage buff affects all sources of Charm, not just Tough Love's. Tough Love's damage buff is affected by the damage modifier cap.

### Dazing Finisher `[Advanced]`
- **설명**: Flourishing enemies that are charmed by you cause them to not be knocked back and dazed instead. | **요구조건**: `{'stats': {'Charisma': 55}, 'talents': ['Charismatic Cast', 'Chaotic Charm', 'Lasting Charisma', 'Tough Love']}`
- **추가 정보**: Applies Daze for 3.35 seconds on proc. This duration is reduced by 0.02 seconds for every point under 55 Charisma, having a minimum duration of 2.85 seconds at 30 Charisma.

### Christmas Miracle `[Spec]`
- **설명**: Christmas Mod Shop reward. Regens hunger and thirst. "Thank you so much K1!" Heh, no problem guys. All in a day's work. | **요구조건**: `{'objectives': ['MODSHOPREWARD']}`

### Freezing Wight `[Common]`
- **설명**: Your Haunted Gale now procs Chilled. | **요구조건**: `{'stats': {'Frostdraw': 40}, 'talents': ['Haunted Gale']}`
- **추가 정보**: Applies Chill for 7 seconds or 1 Crystal on proc. Additionally, this adds the Frostdraw damage type to your Ghosts/Apparitions. Also procs on Specter Apparitions.

### Destructive Recovery `[Rare]`
- **설명**: [Greatsword] Enemies recover 20% less Posture when parrying. | **요구조건**: `{'stats': {'Strength': 25, 'Heavy Weapon': 40}, 'weaponType': 'Greatsword'}`

### Heavy Hitter `[Common]`
- **설명**: [Heavy Weapons] Your posture damage is increased by 5%. | **요구조건**: `{'stats': {'Heavy Weapon': 25, 'Strength': 15}}`

### Lord's Tithe `[Rare]`
- **설명**: Everyone you Reinforce is drained of their Ether while Reinforced. Drain scales with your Shadowcast. Drain health from PvE opponents as well. | **요구조건**: `{'stats': {'Shadowcast': 40, 'Fortitude': 40}, 'mantras': ['Reinforce']}`
- **추가 정보**: Steals Ether (or health in PvE) in pulses.

### Grand Support `[Rare]`
- **설명**: Everyone you buff with Reinforce is healed lightly. You're healed slightly if you heal others. | **요구조건**: `{'stats': {'Fortitude': 40}, 'mantras': ['Reinforce']}`
- **추가 정보**: Heals you for 2% of your maximum health, increased by 1% for every player buffed. Heals affected players by 3% of their maximum health.

### Oath: Contractor `[Oath]`
- **설명**: Your heart is forever now eternally tied to Zi'eer, the 4th Prophet of the Ministry. You swear to serve under his will, no matter the cost. | **요구조건**: `{'talents': ['Oath: Contractor'], 'objectives': ['Good Etris & Ministry reputation and talk to yunshul']}`

### Hidden Tendril `[Oath]`
- **설명**: Landing any physical mantra places a Hidden Tendril on the opponent. | **요구조건**: `{'talents': ['Oath: Contractor'], 'or': [{'slay': '3 players with Oaths in Depths'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Also procs on physical critical attacks, uppercuts, and flourishes.

### String Trick `[Oath]`
- **설명**: Pulls together any two opponents you've attached Hidden Tendril to. | **요구조건**: `{'talents': ['Oath: Contractor'], 'or': [{'slay': 'Grip 3 players with Oaths in Depths'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Does not proc on non-humanoids. Deals a small amount of damage on proc.

### Pressure Detonation `[Common]`
- **설명**: Block breaking an opponent with a Shadow mantra generates a small vacuum that suffocates those hit and steals their Tempo. | **요구조건**: `{'stats': {'Galebreathe': 60, 'Shadowcast': 40}}`
- **추가 정보**: If the user has the Apparitions Talent, this can proc apparitions by inflicting suffocation.

### Finishing Touch `[Common]`
- **설명**: [Dagger] Instantly execute enemies finished with the critical attack of your dagger. | **요구조건**: `{'stats': {'Light Weapon': 40, 'Agility': 50}, 'weaponType': 'Dagger'}`
- **추가 정보**: Your critical must knock the opponent for this Talent to proc.

### Knife's Journey `[Rare]`
- **설명**: [Dagger] Cancelling an enemy's Mantra windup with your Basic Attacks now deals 15% more damage | **요구조건**: `{'stats': {'Light Weapon': 30}}`
- **추가 정보**: In PvE, your Dagger attacks have a 15% chance to critically hit, dealing 5x damage. This does not proc "on critical attack" effects, and cannot proc on Moppet's critical attack.

### Successive Throw `[Common]`
- **설명**: [Dagger] When you successfully flourish an enemy, you throw out a dagger afterwards | **요구조건**: `{'stats': {'Light Weapon': 35}}`
- **추가 정보**: There is a 1.5 second delay after your flourish before the dagger is thrown. This deals 5 Slash damage.

### Chilling Flourish `[Common]`
- **설명**: When flourishing an enemy, they leave behind a trail of ice in the direction you send them. | **요구조건**: `{'stats': {'Frostdraw': 30}}`
- **추가 정보**: Leaves 3-4 ice patches on the ground.

### Spike Traps `[Common]`
- **설명**: Press F during the wind up of your Ice Spikes to create traps around you instead of spawning a spike in the normal spot. | **요구조건**: `{'stats': {'Frostdraw': 30}, 'mantras': ['Ice Spikes']}`
- **추가 정보**: Spikes activate upon being stepped on.

### Condensation Drip `[Common]`
- **설명**: Passively collect condensation from the air, greatly reducing your thirst. | **요구조건**: `{'stats': {'Frostdraw': 15, 'Intelligence': 20}}`
- **추가 정보**: Reduces the passive thirst drain by 3x.

### Cool Head `[Common]`
- **설명**: If set on fire while on ice, immediately put it out and gain the Cool Head status for 30s. During Cool Head, you cannot be lit on fire. | **요구조건**: `{'stats': {'Frostdraw': 30}}`
- **추가 정보**: 15 second cooldown, starting when the effect ends.

### Fragile Freeze `[Common]`
- **설명**: Your Basic Attacks and Criticals now apply Frozen to Chilled opponents on guardbreak. | **요구조건**: `{'stats': {'Frostdraw': 60}}`
- **추가 정보**: Encases them in ice, removing their ability to move, parry, block, or dodge for a short amount of time. Taking damage by any non-Frostdraw damage source (including damage over time effects) will end the freeze early. You can spam Parry, Dodge, or Jump to get out of Freeze faster.

### Preceding Chill `[Rare]`
- **설명**: Enemies hit during the last moments of your ice beam are frozen. | **요구조건**: `{'stats': {'Frostdraw': 60}, 'mantras': ['Ice Beam']}`
- **추가 정보**: If the user has Crystallization, this Talent no longer freezes but instead causes crystals to explode.

### Golden Age `[Common]`
- **설명**: Your Iron Pull now detonates Crystals and overloads Surges. | **요구조건**: `{'talents': ['Gilded Path: Scrapsinger', 'Glass Path: Crystallization', 'Surge Path: Unstable Capacitor']}`

### Blood Thirsty `[Common]`
- **설명**: Gain a speed boost after causing an opponent heavy blood loss. | **요구조건**: `{'stats': {'Agility': 45}}`

### In a Hurry `[Common]`
- **설명**: You grip faster with a movement speed boost. | **요구조건**: `{'stats': {'Agility': 30}}`
- **추가 정보**: Reduces grip time by 0.5 seconds (16.67% faster).

### Muffled Screams `[Common]`
- **설명**: You quieten the cries of help of those you execute, reducing the distance at which their allies will hear it and come to assist, and reducing the effectiveness of Talents that slow your executions. | **요구조건**: `{'stats': {'Agility': 50}}`
- **추가 정보**: NPCs have a shortened aggro range from gripping allies in proximity. Defiant Until The End and Last Second Negotiations affect your grip speed less.

### Blighted Song `[Common]`
- **설명**: Attaching your Shadow Chains to enemies disables yours and the enemy's ability to cast mantras. You take reduced damage from enemies while this is applied. | **요구조건**: `{'stats': {'Fortitude': 10, 'Shadowcast': 1}, 'mantras': ['Shadow Chains']}`
- **추가 정보**: Grants the user and the chained opponent 20% damage reduction against outside attacks.

### Dark God `[Common]`
- **설명**: If a Shadowcast mantra would drin your opponent's Ether to 0, drain from their Tempo instead and increase your Tempo. Shadowcast mantras will now raise your tempo if your ether is full. | **요구조건**: `{'stats': {'Shadowcast': 20}}`

### Dark Synergy `[Common]`
- **설명**: Engulf your enemy in shadows when flourishing them. | **요구조건**: `{'stats': {'Shadowcast': 45}, 'talents': ['Dark God']}`
- **추가 정보**: Deals 5 Shadowcast damage on proc.

### Dark Waltz `[Common]`
- **설명**: Anytime you guardbreak your opponent with a light attack or critical, steal half of your opponent's current tempo. Also apply Ether Sunder to PvE enemies. | **요구조건**: `{'stats': {'Weapon': 90, 'Shadowcast': 90}}`

### Dark Hours `[Common]`
- **설명**: Your Shadowcast Mantras deal 15% more damage at night and in realms the Sun does not reach. | **요구조건**: `{'stats': {'Shadowcast': 35}}`
- **추가 정보**: Night cycle is XX:50 to XX:10 in real-time.

### Dark Rift `[Rare]`
- **설명**: Enter a rifted state when you successfully dodge, where you can't be damaged until its duration ends. Can be cancelled early if you attack. | **요구조건**: `{'stats': {'Shadowcast': 60}, 'talents': ['Dark Hours']}`
- **추가 정보**: Lasts 1.8 seconds with a 20 second cooldown that starts on proc. Blocking, parrying, dodging, or sliding will also cancel the effect. You cannot use Mantras during Dark Rift.

### Night Terror `[Common]`
- **설명**: Your light attacks now proc Fear the Dark. | **요구조건**: `{'stats': {'Weapon': 100, 'Shadowcast': 100}, 'talents': ['Fear the Dark']}`
- **추가 정보**: Also procs on weapon criticals. Despite its description, this Talent immediately applies the Fear status for 1 second with no cooldown (they are not required to run away from you).

### Overwhelming Drain `[Common]`
- **설명**: If multiple enemies are hit by your Shadow Eruption, they are Dazed for 0.7s. | **요구조건**: `{'stats': {'Shadowcast': 1}, 'mantras': ['Shadow Eruption']}`

### Shadow Overflow `[Common]`
- **설명**: Extra ether stolen with mantras are exerted as dark energy, damaging and absorbing ether from those nearby. | **요구조건**: `{'stats': {'Shadowcast': 55}, 'talents': ['Dark God']}`
- **추가 정보**: Has a 4 second cooldown. Deals 5 Shadowcast damage on proc.

### Oath: Dawnwalker `[Oath]`
- **설명**: You vow to forever reach towards the brilliant Light. There is no shadow that your radiance cannot expunge. | **요구조건**: `{'stats': {'Power': 10}, 'objectives': ['30 Medallions and Speak to Klaris']}`

### Absolute Radiance `[Oath]`
- **설명**: Dealing damage with Dawnwalker mantras briefly makes you immune to all elemental effects for a short period. | **요구조건**: `{'talents': ['Oath: Dawnwalker'], 'or': [{'objectives': ['Pay 60 Medallions']}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: All elemental status effects cannot be applied to you during Absolute Radiance.

### Protagonist Syndrome `[Oath]`
- **설명**: The grasp of shadow is meaningless in the face of your blinding light. Your Dawnwalker mantras are empowered after getting hit by Shadowcast. | **요구조건**: `{'talents': ['Oath: Dawnwalker'], 'or': [{'objectives': ['Pay 60 Medallions']}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Increases your Dawnwalker Mantra damage by 30% after being hit by Shadowcast damage. This cannot be self procced by using Shade Devour.

### Luminous Flash `[Oath]`
- **설명**: After dealing a certain amount of damage in Absolute Radiance, gain a chance to empower your strikes with pure light. | **요구조건**: `{'talents': ['Oath: Dawnwalker'], 'or': [{'objectives': ['Pay 60 Medallions']}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: During Absolute Radiance, your M1 attacks have a chance to proc Luminous Flash, applying the damage modifier hardcap as a damage buff.

### Blackhole `[Common]`
- **설명**: Your singularity pulls everyone nearby in. | **요구조건**: `{'stats': {'Power': 13, 'Shadowcast': 60}, 'talents': ['Singularity']}`
- **추가 정보**: Pulls anyone nearby in a medium sized aoe to the closest opponent you hit with a shadow mantra.

### Energy Siphon `[Common]`
- **설명**: Your singularity now pulls ether from the extra players affected by Blackhole. | **요구조건**: `{'stats': {'Shadowcast': 60}, 'talents': ['Black Hole', 'Singularity']}`
- **추가 정보**: Takes 15 Ether from the affected opponent on proc.

### Call of the Deep `[Origin]`
- **설명**: Sink beneath the waves and return to the Depths | **요구조건**: `{'origin': 'Deepbound'}`
- **추가 정보**: When used in the overworld, play an animation and sink into the first layer. This does not count as a drown. When used in the Depths, teleport to Castle Light with a 20 minute cooldown.

### Deepbound Contract `[Origin]`
- **설명**: You progress much faster in the Depths, and slower on the overworld. You can regain sanity at Castle Light, but will always face the strongest foes in your Trial. | **요구조건**: `{'origin': 'Deepbound'}`
- **추가 정보**: You can always enter Castle Light, even if you've drowned. Your Depths trial will always be an Enforcer or harder.

### Spell Shout `[Quest]`
- **설명**: You will now shout your mantra name upon cast
- **추가 정보**: The player will say the name of the Mantra they cast in a chat bubble. e.g. casting Fire Blade will make the player say "Fire Blade!" Renaming a Mantra will Spell Shout the new Mantra name.

### Frozen Web `[Common]`
- **설명**: Landing a critical with a Static Link on your opponent applies Chilled. | **요구조건**: `{'stats': {'Frostdraw': 40, 'Thundercall': 40}, 'talents': ['Static Link']}`
- **추가 정보**: Applies Chill for 7 seconds and Bottom Freeze. Has a 4 second cooldown.

### Buster Call `[Faction]`
- **설명**: Radio in the Authority's navy for a buster call, sending out a barrage of bombardment wherever you see fit. | **요구조건**: `{'objectives': ['Command Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: Grants a Talent tool that lights a flare and highlights a large AoE on the ground. After a considerable delay, that location will be bombed several times, dealing very high damage. Cannot directly knock players. Applies burn on hit. 24 hour cooldown.

### Officer's Slash `[Faction]`
- **설명**: You now gain an additional critical attack with Authority armory weaponry while your regular critical attack is on cooldown. | **요구조건**: `{'objectives': ['Command Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: Deals 35 Slash damage. 20 second cooldown.

### Officer's Training `[Faction]`
- **설명**: While using a Sword or Rapier, take 30% less posture damage from criticals. | **요구조건**: `{'objectives': ['Command Division'], 'origin': 'Authority Ensign'}`

### Target Focus `[Faction]`
- **설명**: Enemies you charm take more damage from your squadmates in your party. | **요구조건**: `{'objectives': ['Command Division'], 'origin': 'Authority Ensign'}`

### Ethiron's Gaze `[Quest]`
- **설명**: Your eyes have been opened to the wasteland. You can see through the harsh fog of the storm of the Eternal Gale more clearly now. | **요구조건**: `{'quests': ['Complete Erosius Amaltus Univortus Casius Walistoshus Quest']}`
- **추가 정보**: The snow in the Second Layer no longer affects your ability to see. Also reduces the visual clutter of snow in the overworld.

### Concussion `[Rare]`
- **설명**: Enemies you flourish into walls have their vision altered for a short duration and are dazed longer than usual. Flourished PvE enemies get Stagger for a few seconds. | **요구조건**: `{'stats': {'Strength': 20, 'Fortitude': 15}}`

### Concussive Force `[Common]`
- **설명**: Enemies you knocked remain downed longer than usual. | **요구조건**: `{'stats': {'Strength': 15}}`
- **추가 정보**: Enemies remain knocked for 15 seconds instead of 10.

### Precise Swing `[Common]`
- **설명**: After landing a critical your next basic attack will gain 25% chip past your opponent's block. | **요구조건**: `{'stats': {'Strength': 25, 'Agility': 15}}`
- **추가 정보**: Procs even if your critical is parried or blocked. The Precise Swing status effect will be lost should your next M1 land or get parried. This is additive with all other sources of Chip Damage.

### Spine Cutter `[Rare]`
- **설명**: Hitting an enemy in the back after a roll cancel will initiate a second attack that deals your weapon's raw damage. | **요구조건**: `{'stats': {'Strength': 20, 'Agility': 25}}`
- **추가 정보**: The second slash has no PEN. Procs on certain physical Mantras and criticals with the M1 tag. Has a 5 second cooldown.

### Steady Nerves `[Common]`
- **설명**: You dance from toe to toe - successful dodges restore posture. | **요구조건**: `{'stats': {'Strength': 15, 'Agility': 45}}`
- **추가 정보**: Restore 2 flat posture on a successful dodge.

### Strong Hold `[Common]`
- **설명**: [Medium Weapons] When above half health and two-handing, posture damage taken is reduced by 5%. | **요구조건**: `{'stats': {'Medium Weapon': 30, 'Strength': 30}}`

### Strong Stern `[Rare]`
- **설명**: The duration you are dazed from wall bangs is cut in half. Slightly reduce your guardbreak stun time from PvE enemies as well. | **요구조건**: `{'stats': {'Strength': 15, 'Fortitude': 25}}`

### Tap Dancer `[Rare]`
- **설명**: Dodging immediately after a roll-cancel no longer puts your Dodge on a longer cooldown. | **요구조건**: `{'stats': {'Agility': 60}}`
- **추가 정보**: Negate the extra half a second cooldown added to the roll following a roll-cancel.

### Concussive Flash `[Common]`
- **설명**: Your blinding light now concusses foes. | **요구조건**: `{'stats': {'Flamecharm': 30, 'Strength': 25}, 'mantras': ['Flame Blind']}`
- **추가 정보**: People blinded by Flame Blind are Dazed for 2 seconds.

### Charged Return `[Common]`
- **설명**: Being under an elemental status effect causes your Basic Attacks and Criticals to do 10% more damage. | **요구조건**: `{'stats': {'Willpower': 20, 'Strength': 15}}`
- **추가 정보**: Procs on Burn, Chill, Shock, Fear, Winded, and Suffocation.

### Nullifying Clarity `[Common]`
- **설명**: Deal 10% more damage to enemies with elemental status effects, but remove the status on hit. | **요구조건**: `{'stats': {'Strength': 15, 'Intelligence': 5}}`
- **추가 정보**: Procs on Burn, Chill, Shock, Fear, Winded, and Suffocation. Only works on M1s.

### Cornered Fool `[Common]`
- **설명**: Blockbreaking a Charmed opponent procs Taunt for 5s, making them take and deal more damage. | **요구조건**: `{'stats': {'Charisma': 85}, 'mantras': ['Taunt']}`
- **추가 정보**: Despite what the description states, this applies Taunt for 6 seconds. Every point of Charisma below 85 will reduce the duration of this Taunt by 0.035 seconds, capping at a minimum of 5.12 seconds with 60 Charisma. The Taunt damage buff is also applied to the attack that guard broke. 15 second cooldown.

### Give and Take `[Common]`
- **설명**: Deal less damage to comrades and receive less damage from comrades. | **요구조건**: `{'stats': {'Charisma': 35}}`
- **추가 정보**: This does not apply to self damage. Stacks multiplicatively with Loyalty.

### Off Your Game `[Common]`
- **설명**: You now slow Taunted enemies when you hit them. | **요구조건**: `{'stats': {'Charisma': 90}, 'mantras': ['Taunt']}`

### Robber Baron `[Common]`
- **설명**: Halves the number of items you drop on death. You no longer lose Notes on death.
- **추가 정보**: Lose 25% of your non-Soulbound/Enchanted items on death instead of 50%.

### Ether Absorption `[Common]`
- **설명**: Receive Ether back when inflicted with damage from Mantras. | **요구조건**: `{'stats': {'Intelligence': 15}}`

### Eureka `[Rare]`
- **설명**: Gain a stack of Inspiration every time you land or parry a Mantra. Whiffing a Mantra removes a stack of Inspiration. Reaching 3 stacks grants +10% Mantra Damage to your next Mantra attack. | **요구조건**: `{'stats': {'Intelligence': 30}}`
- **추가 정보**: Landing and parrying Mantras grants Inspiration stacks. Mantras cap at giving 1 stack per, and you do not gain stacks from autoparry frames.

### Keen Recovery `[Common]`
- **설명**: Landing a basic attack after feinting a mantra will restore the feinted mantra's ether cost. | **요구조건**: `{'stats': {'Intelligence': 55}}`
- **추가 정보**: The ether restored scales on your Intelligence. At 55 Intelligence this will restore 100% of the Mantra's Ether cost, scaling up or down if you have more or less than this Intelligence investment.

### Behind You `[Common]`
- **설명**: Landing a basic attack behind your enemy after feinting a mantra will apply an ether slash, dealing extra damage based on how much ether you have left. | **요구조건**: `{'stats': {'Intelligence': 70, 'Agility': 40}, 'talents': ['Keen Recovery']}`
- **추가 정보**: Deals 15 physical damage when at full Ether.

### Unwavering Focus `[Common]`
- **설명**: When your mantras are parried, receive less posture (scales with intelligence). | **요구조건**: `{'stats': {'Intelligence': 60, 'Strength': 10}}`
- **추가 정보**: Grants 0.3% posture resistance per point in Intelligence, capping at +21% at 70 Intelligence.

### Reverse Leech `[Common]`
- **설명**: Anytime you proc Behind You, steal ether from your opponent too. | **요구조건**: `{'stats': {'Shadowcast': 60}, 'talents': ['Behind You']}`
- **추가 정보**: Behind You is procced by landing a basic attack behind your enemy after feinting a Mantra.

### Oath: Fadetrimmer `[Oath]`
- **설명**: You vow to forever hone your precision with the scissors. There will never be another fringe incident again. | **요구조건**: `{'stats': {'Power': 12}, 'objectives': ['Change your appearance 12 Times']}`

### Barber's Skillset `[Oath]`
- **설명**: What type of look are we going for today? | **요구조건**: `{'talents': ['Oath: Fadetrimmer']}`
- **추가 정보**: Gives a Talent tool that opens an outdated version of the Barber UI. When selecting others: Changes what haircut your Fadetrimmer Mantras apply on hit. When selecting yourself: Changes your own hair.

### Hair Product `[Oath]`
- **설명**: What's in these things? | **요구조건**: `{'talents': ['Oath: Fadetrimmer']}`
- **추가 정보**: Gives a Talent tool that shows a popup menu and allows you to select either Flammable, Charming, or Revitalizing Hair Sprays. Your Hair Spray will change to the chosen effect.

### Hair Spray `[Oath]`
- **설명**: Apply your Hair Products. | **요구조건**: `{'talents': ['Oath: Fadetrimmer']}`
- **추가 정보**: Flammable applies Burn or causes an Eruption; parryable and blockable. Charming applies Charm for 15 seconds; parryable and blockable. Revitalizing heals 10% of the affected entity's health; unparryable and unblockable. 10 second cooldown.

### Meteor Impact `[Common]`
- **설명**: Aerial moves you land will follow up into a devastating slam. This is also possible when you yourself gets hit by an aerial move. | **요구조건**: `{'stats': {'Flamecharm': 25}, 'objectives': ['Any Rising Mantra']}`
- **추가 정보**: Deals 10 flat Flamecharm damage on top of your weapon's scaled damage. Procs by light attacking after using certain Mantras that end with both the user and the victim suspended in the air.

### Phoenix Impact `[Common]`
- **설명**: If you Meteor Slam an opponent whilst on fire, restore some HP and Ether. | **요구조건**: `{'stats': {'Flamecharm': 40}, 'talents': ['Meteor Impact']}`
- **추가 정보**: Heals 4% max HP and restores 20 ether.

### Fang and Coil `[Quest]`
- **설명**: Adopt the path of the serpent. | **요구조건**: `{'slay': 'Doom of Caeranthil', 'or': [{'stats': {'Light Weapon': 20}, 'objectives': ['Speak to Vesque while having ally Etrea reputation']}, {'objectives': ['Spawn in with the Fang and Coil Fist style']}]}`
- **추가 정보**: Allows you to use the Fang and Coil fist style.

### Fishman `[Rare]`
- **설명**: When your Blood is over 50%, you won't drown when Unconscious in water. Gain additional healing from knocking others Unconscious in water.

### Landshark `[Quest]`
- **설명**: Killing a Megalodaunt will grant lifesteal on your attacks for 30 seconds. | **요구조건**: `{'objectives': ['Unobtainable']}`
- **추가 정보**: The lifesteal only works in PvE.

### Dancing Steps `[Common]`
- **설명**: Fire mantras now move you in the direction you're facing. | **요구조건**: `{'stats': {'Power': 8, 'Flamecharm': 35}}`
- **추가 정보**: Casting a Flamecharm Mantra will give you a moderate boost of horizontal movement in the direction your character is facing. This will still proc even if the Mantra is feinted. 5 second cooldown.

### Graceful Steps `[Rare]`
- **설명**: Your dancing steps now gives a faster speed boost. | **요구조건**: `{'stats': {'Power': 8, 'Flamecharm': 80}, 'talents': ['Dancing Steps']}`
- **추가 정보**: The speed boost has a very short duration; having a fast swingspeed weapon is recommended to capitalize off this Talent's effect. 5 second cooldown.

### The Final Act `[Rare]`
- **설명**: Landing a fire mantra immediately after flourishing an opponent will cause them to explode. | **요구조건**: `{'stats': {'Power': 13, 'Flamecharm': 60}}`
- **추가 정보**: Deals 5 Flamecharm damage on proc.

### Cauterized Wounds `[Common]`
- **설명**: Blood loss from all sources is lowered. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Fortitude': 5}}`
- **추가 정보**: Does not reduce the blood damage of 'blood drain' effects, such as casting or being hit by Bloodrend Mantras, blood drain potions, and the blood loss Corrupt Resonance downside. Stacks multiplicatively with Alloyblood. The effectiveness of this Talent is reduced if you are using the Curse of the No Life King enchantment.

### Warding Radiance `[Rare]`
- **설명**: Every fire mantra builds up one halo stack. At 3 stacks a halo appears that allows you to slide further. Hell's Partisan is also triggered passively while this is active. | **요구조건**: `{'stats': {'Flamecharm': 30, 'Agility': 20}}`
- **추가 정보**: Allows you to proc Hell's Partisan on Flamecharm Mantras that aren't Fire Forge while you have the halo active. Lasts 60 seconds, but cannot be refreshed.

### Flamewalker `[Common]`
- **설명**: When Warding Radiance is active you leave trails of flame when you slide. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Agility': 25}, 'talents': ['Warding Radiance']}`

### Hell's Partisan `[Common]`
- **설명**: After landing a flame dagger on an opponent, your next hit against them will impale with a divine spear from above. | **요구조건**: `{'stats': {'Flamecharm': 35}, 'or': [{'talents': ['Warding Radiance']}, {'mantras': ['Fire Forge']}]}`
- **추가 정보**: Deals 5 Flamecharm damage. Parryable, but not blockable or dodgeable due to hitstun.

### Flamecharm Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Flamecharm to its fullest. | **요구조건**: `{'stats': {'Flamecharm': 75}, 'talents': ['Master Flamecharmer'], 'slay': 'Any humanoid boss'}`
- **추가 정보**: Removes the 75 investment cap on the Flamecharm Attribute. This Talent will be removed if you do not meet its stat requirements.

### Flamecharmer `[Common]`
- **설명**: Grants you the ability to command Fire as a Flamecharmer. | **요구조건**: `{'stats': {'Flamecharm': 1}}`

### Adept Flamecharmer `[Common]`
- **설명**: You can now obtain 1-Star Leveled Flamecharmer Mantras. | **요구조건**: `{'stats': {'Flamecharm': 20}, 'talents': ['Flamecharmer']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Expert Flamecharmer `[Common]`
- **설명**: You can now obtain 2-Star Leveled Flamecharmer Mantras. | **요구조건**: `{'stats': {'Flamecharm': 30}, 'talents': ['Adept Flamecharmer']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Master Flamecharmer `[Common]`
- **설명**: You can now obtain 3-Star Leveled Flamecharmer Mantras. | **요구조건**: `{'stats': {'Flamecharm': 50}, 'talents': ['Expert Flamecharmer']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Azure Flames `[Common]`
- **설명**: Many of your flames turn blue, signifying their increased intensity. | **요구조건**: `{'stats': {'Flamecharm': 70, 'Willpower': 40}}`
- **추가 정보**: Increases burn damage by 12.5%. Increases the radius and posture damage of Eruptions. Increases Flame of Denial's duration by 25%.

### Temperature Shock `[Common]`
- **설명**: Your fire mantras now detonate any stacked crystals. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Frostdraw': 40}, 'talents': ['Glass Path: Crystallization']}`
- **추가 정보**: This has a 4 second cooldown.

### Exoskeleton `[Rare]`
- **설명**: You have a layer of fortified Natural Armor that replenishes when you rest. Your Natural Armor will resist 10% Physical Damage when active. | **요구조건**: `{'stats': {'Fortitude': 40}}`
- **추가 정보**: Exoskeleton's resistance will be less effective if you do not meet its Fortitude requirement, losing 0.125% resistance for every point under 40 Fortitude, capping at 6.875% resistance with 15 Fortitude. Chitin's resistances stack multiplicatively with Exoskeleton.

### Glacial Mobility `[Common]`
- **설명**: Cast while slide-jumping to perform a running attack with your ice sabers. | **요구조건**: `{'stats': {'Frostdraw': 20, 'Agility': 20}, 'mantras': ['Ice Blade']}`
- **추가 정보**: The Talent activates after you've slide jumped, and not during the slide jump, contrary to the Talent description.

### Frostdraw Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Frostdraw to its fullest. | **요구조건**: `{'stats': {'Frostdraw': 75}, 'talents': ['Master Frostdrawer'], 'slay': 'Any humanoid boss'}`
- **추가 정보**: Removes the 75 investment cap on the Frostdraw Attribute. This Talent will be removed if you do not meet its stat requirements.

### Frostdrawer `[Common]`
- **설명**: Grants you the ability to command Ice as a Frostdrawer. | **요구조건**: `{'stats': {'Frostdraw': 1}}`

### Adept Frostdrawer `[Common]`
- **설명**: You can now obtain 1-Star Leveled Frostdrawer Mantras. | **요구조건**: `{'stats': {'Frostdraw': 20}, 'talents': ['Frostdrawer']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Expert Frostdrawer `[Common]`
- **설명**: You can now obtain 2-Star Leveled Frostdraw Mantras. | **요구조건**: `{'stats': {'Frostdraw': 30}, 'talents': ['Adept Frostdrawer']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Master Frostdrawer `[Common]`
- **설명**: You can now obtain 3-Star Leveled Frostdraw Mantras. | **요구조건**: `{'stats': {'Frostdraw': 50}, 'talents': ['Expert Frostdrawer']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Cold Front `[Common]`
- **설명**: Your vent is imbued with glacial frost. | **요구조건**: `{'stats': {'Frostdraw': 25}}`
- **추가 정보**: Venting creates an ice patch on the floor and applies Chill to any enemy hit by it. Increases your Vent damage by 40% and changes its damage type to Frostdraw.

### Fulgurite Formation `[Common]`
- **설명**: When your Crystals explode, lightning strikes. When your Surge charges Overload on an enemy, your Crystals apply twice on them for 8s. | **요구조건**: `{'stats': {'Frostdraw': 50, 'Thundercall': 50}, 'talents': ['Glass Path: Crystallization', 'Surge Path: Unstable Capacitor']}`
- **추가 정보**: The lightning strikes deal 5 typeless damage with a 4 second cooldown. The double Crystal application buff does not stack with successive Fulgurite Formation procs. Procs Grounding Bolt.

### Orbital Ice `[Common]`
- **설명**: When landing a parry while standing on ice, automatically form a ring of ice that grants 15% Physical Resistance. The ring will break after sustaining a certain amount of damage, scaling with your Frostdraw. | **요구조건**: `{'stats': {'Frostdraw': 65}}`
- **추가 정보**: 90 second cooldown. Durability of Orbital Ice is equal to "Frostdraw investment +10".

### Glacial Coasting `[Common]`
- **설명**: Sliding while Orbital Ice is active leaves trails of ice. | **요구조건**: `{'stats': {'Agility': 25, 'Frostdraw': 50}, 'talents': ['Orbital Ice']}`

### Frozen Legs `[Rare]`
- **설명**: Chilled applied by Mantras prevents your opponents from rolling. | **요구조건**: `{'stats': {'Frostdraw': 60}}`
- **추가 정보**: Lasts for 0.75 seconds.

### Imperium Kata `[Quest]`
- **설명**: Wield an advanced form of the Legion's martial arts | **요구조건**: `{'objectives': ['Obtain the Legion Intelligence, defeat Titus, return to Caitus']}`
- **추가 정보**: Allows you to use the Imperium Kata fist style.

### Legion Kata `[Quest]`
- **설명**: Gain the ability to use the Legion's martial arts. | **요구조건**: `{'objectives': ["Talk with Amara while having Captain's Rec in your inventory."]}`
- **추가 정보**: Allows you to use the Legion Kata fist style.

### Galebreathe Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Galebreathe to its fullest. | **요구조건**: `{'stats': {'Galebreathe': 75}, 'talents': ['Master Galebreather'], 'slay': 'Any humanoid boss'}`
- **추가 정보**: Removes the 75 investment cap on the Galebreathe Attribute.

### Galebreather `[Common]`
- **설명**: Grants you the ability to command wind as a Galebreather. | **요구조건**: `{'stats': {'Galebreathe': 1}}`

### Adept Galebreather `[Common]`
- **설명**: You can now obtain 1-Star Leveled Galebreathe mantras. | **요구조건**: `{'stats': {'Galebreathe': 20}, 'talents': ['Galebreather']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Expert Galebreather `[Common]`
- **설명**: You can now obtain 2-Star Leveled Galebreathe mantras. | **요구조건**: `{'stats': {'Galebreathe': 30}, 'talents': ['Adept Galebreather']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Master Galebreather `[Common]`
- **설명**: You can now obtain 3-Star Leveled Galebreathe mantras. | **요구조건**: `{'stats': {'Galebreathe': 50}, 'talents': ['Expert Galebreather']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### After Cut `[Common]`
- **설명**: If an attack is physical and wind it will apply an after cut that does 5% of the damage you dealt. If an attack was a mantra, it does 2.5% damage instead. | **요구조건**: `{'stats': {'Galebreathe': 40}}`
- **추가 정보**: The damage After Cut deals is based on the attack's final damage, post modifiers and resistances.

### Breathing Impact `[Common]`
- **설명**: Knocking enemies into objects with wind spells deals additional blunt damage based on how hard they're hit. | **요구조건**: `{'stats': {'Galebreathe': 30}}`
- **추가 정보**: The increased damage dealt is based on the attack's initial damage and your opponent's acceleration. Very ping/server reliant.

### Inhale `[Common]`
- **설명**: Canceling a Wind Mantra stores it for 5 seconds, empowering the next Wind Mantra cast in that time. [7 sec CD, gets removed upon landing a light attack] | **요구조건**: `{'stats': {'Galebreathe': 60}}`
- **추가 정보**: Inhaling adds (Mantra level multiplied by 2)% damage to the next Galebreathe Mantra cast. Grants a speed boost for 3 seconds. Additionally grants the Maestro's Blade status effect, allowing your basic attacks to proc After Cut. The Mantra modifiers on the inhaled Mantra are passed onto the next eligible Mantra cast.

### Neuroplasticity `[Rare]`
- **설명**: Your mind is a pliable, flexible substance. The Ether cost of additional modifications to your Mantras is now reduced by 10%. | **요구조건**: `{'stats': {'Mind': 35}}`
- **추가 정보**: The reduced cost on Mantra modifiers does not apply retroactively to previously modified Mantras until you rejoin.

### Glass Path: Crystallization `[Common]`
- **설명**: Your ice abilities no longer grant a slow effect or the ability to freeze and instead cause ice crystals to grow on your opponent. | **요구조건**: `{'stats': {'Frostdraw': 40}}`
- **추가 정보**: Turns your Frostdraw pink. Applying chill or freeze applies red ice crystals on the enemy instead of slowing opponent. Stacking 5 ice crystals or guard breaking an opponent who has crystals makes them explode. Each crystal has 3 base damage with 5 Frostdraw scaling, increasing by 0.015 damage per Frostdraw investment for a maximum damage of 4.5 each at 100 Frostdraw. 1 second cooldown on explosion proc.

### Crystal Shrapnel `[Common]`
- **설명**: Your crystal explosions now have an AoE that applies crystals to all hit. | **요구조건**: `{'stats': {'Frostdraw': 60}, 'talents': ['Glass Path: Crystallization']}`
- **추가 정보**: Does not hit allies or the target you procced the Crystal explosion on. Scales off Frostdraw investment and amount of crystals present.

### Reclaimed Glass `[Common]`
- **설명**: Your Crystal Shrapnel explosions now grant you and any allies caught in them 10% Elemental Resistance for 10 seconds. | **요구조건**: `{'stats': {'Frostdraw': 65}, 'talents': ['Crystal Shrapnel']}`
- **추가 정보**: The duration of this effect is refreshable by reproccing it.

### Fortitude Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your fortitude to its fullest. | **요구조건**: `{'stats': {'Fortitude': 75}, 'objectives': ['Speak to Brutus']}`
- **추가 정보**: Removes the 75 investment cap on the Fortitude Attribute. The stat requirements to obtain this Talent will be increased to 77 or 78 if your Aspect has increased Fortitude on spawn, though this limitation will be removed if you have the Multifaceted Echo Unlock. The quest requirement for this Talent will be removed if you've obtained it previously on your account.

### Bodkin Arrow `[Rare]`
- **설명**: Your charged shots now do extra armor damage to armored enemies and extra damage to unarmored enemies. | **요구조건**: `{'stats': {'Strength': 55}, 'weaponType': 'Bow'}`

### Hard Stop `[Rare]`
- **설명**: Landing a charged shot will knock your opponent back. | **요구조건**: `{'talents': ['Bodkin Arrow'], 'weaponType': 'Bow'}`

### Precision Crusher `[Rare]`
- **설명**: Landing a charged shot will knock your opponent down instead of back. | **요구조건**: `{'stats': {'Strength': 75}, 'talents': ['Hard Stop'], 'weaponType': 'Bow'}`

### Armor Piercing `[Rare]`
- **설명**: [Guns] Your gun attacks now ignore 10% of an opponent's blunt armor. Applied Multiplicatively before PEN is applied. | **요구조건**: `{'stats': {'Weapon': 30}, 'quests': ['Trig Quest'], 'or': [{'weaponType': 'Greatcannon'}, {'weaponType': 'Pistol'}, {'weaponType': 'Rifle'}]}`
- **추가 정보**: This has heavy diminishing returns in effectiveness with the more PEN you have. Elemental guns may not benefit from this Talent at all depending on your opponent's resistances, as the highest resistance value is prioritized.

### Execution `[Rare]`
- **설명**: Your offhand gun attacks now count as flourishes and do a flat 20 extra damage when used with no bullets. | **요구조건**: `{'stats': {'Light Weapon': 90}, 'weaponType': 'Pistol', 'or': [{'stats': {'Medium Weapon': 90}}, {'stats': {'Heavy Weapon': 90}}]}`
- **추가 정보**: Deals true damage. Only works if you do not have bullets in your inventory. Also procs on the offhand shots of Dual Gun attacks, but it deals 5 true damage instead if used on Dual Guns.

### Gunpowder Blast `[Common]`
- **설명**: Pistol shots without bullets do 2 extra posture. [Dual Guns] | **요구조건**: `{'stats': {'Light Weapon': 45}, 'weaponType': 'Pistol'}`
- **추가 정보**: Pistol blast shots deal 2 more posture damage if you have no bullets in your inventory.

### Hip Shooter `[Rare]`
- **설명**: When wielded with a Medium/Heavy weapon, your side gun can now fire a bullet projectile. | **요구조건**: `{'stats': {'Light Weapon': 25}, 'weaponType': 'Pistol', 'or': [{'stats': {'Medium Weapon': 50}}, {'stats': {'Heavy Weapon': 50}}]}`
- **추가 정보**: 5 second cooldown. Requires ammunition in your inventory to be used.

### Parting Gift `[Common]`
- **설명**: After you land a flourish, gain the ability to shoot bullets for 5 seconds. [Dual Gun] | **요구조건**: `{'stats': {'Light Weapon': 75}, 'weaponType': 'Pistol'}`
- **추가 정보**: On proc, all dual gun M1s within the next 5 seconds have projectiles.

### True Ether Bullets `[Rare]`
- **설명**: Using Ether Bullets applies elemental damage of your highest investment. | **요구조건**: `{'stats': {'Weapon': 20, 'Intelligence': 30}, 'weaponType': 'Pistol, Rifle, Greatcannon'}`
- **추가 정보**: Landing 2 shots will make the 3rd shot deal elemental damage and apply the status effect correlating to your highest attunement. This Talent will not do anything if you do not have an attunement.

### Prime Ether Bullets `[Advanced]`
- **설명**: Your bullets take one less hit to proc elemental effects and now have slight intelligence scaling. [Dual Gun] | **요구조건**: `{'stats': {'Light Weapon': 90, 'Intelligence': 60}, 'talents': ['True Ether Bullets'], 'weaponType': 'Pistol'}`
- **추가 정보**: True Ether Bullets now procs in 2 hits instead of 3. Adds 1.2 Intelligence scaling to your Pistols.

### Quickdraw `[Common]`
- **설명**: Allows you to fire your offhand gun right after swinging. [Not necessary on dual guns] | **요구조건**: `{'stats': {'Light Weapon': 55}, 'weaponType': 'Pistol'}`
- **추가 정보**: Allows the user to instantly start attacking with their offhand gun after attacking with their main weapon.

### Quick Swap `[Common]`
- **설명**: Massively reduce your bullet swap cooldown. [Dual Gun] | **요구조건**: `{'stats': {'Light Weapon': 40}, 'weaponType': 'Pistol'}`

### Brain Rattler `[Common]`
- **설명**: [Clubs] Guardbreaking an opponent with your Critical rattles their brain in its container, causing increased blood loss, applies Stagger to PvE enemies and blurs their vision. | **요구조건**: `{'stats': {'Medium Weapon': 50}, 'weaponType': 'Club'}`

### Dispatch `[Common]`
- **설명**: [Clubs] Bear Trapped targets deal 20% less posture. Dazed targets deal 20% less posture. This can stack. | **요구조건**: `{'stats': {'Medium Weapon': 55}, 'talents': ['Bear Trap'], 'weaponType': 'Club'}`

### Hammerfall `[Common]`
- **설명**: [Clubs] Aerial attacks do 25% more posture damage when blocked. | **요구조건**: `{'stats': {'Medium Weapon': 35}, 'weaponType': 'Club'}`

### Fan the Flames `[Common]`
- **설명**: Your stored Wind mantras can now empower your Fire mantras. | **요구조건**: `{'stats': {'Flamecharm': 40}, 'talents': ['Inhale']}`
- **추가 정보**: The benefits of Inhale can now be applied to your Flamecharm Mantras.

### All the Dead Gods `[Rare]`
- **설명**: Your Basic Attacks now apply anti-heal and 5% Heal Boost against PvE for 8s. | **요구조건**: `{'stats': {'Willpower': 65, 'Intelligence': 40}}`
- **추가 정보**: Whenever you land a Basic Attack, the target has most healing forms reduced/disabled for 8 seconds. Your anti-heal potency scales on your Willpower + Intelligence investment, only having 100% anti-heal if your Intelligence and Willpower attributes add up to at least 105. Increases the duration of all other Anti-Heal effects you apply by 2 seconds.

### All Above, Gods Below `[Advanced]`
- **설명**: Any healing your opponent were to receive while All The Dead Gods is active on them is stolen and given to you, increase your PvE Heal Boost to 15% as well. | **요구조건**: `{'stats': {'Willpower': 100, 'Intelligence': 100}, 'talents': ['All the Dead Gods']}`
- **추가 정보**: Only applies to "active" healing. The duration of this effect will be reduced if you do not meet the Talent's requirements. This will not proc if you are the one who applied the healing; you cannot heal yourself by healing your opponent.

### Heretic's Sutra `[Quest]`
- **설명**: A chant that steers you into the state of Insanity for 20 seconds. | **요구조건**: `{'stats': {'Willpower': 80}, 'quests': ['Have had tier 1 insanity (shivering), and talk to Kasen, located in Layer 2 Floor 1.']}`
- **추가 정보**: Grants a Talent tool that drains the user's sanity on proc. If your sanity is above 80%, it will be set to 65% on use. If your sanity is below 80%, it will be reduced by 15% on use. Passively procs Shared Misery and Piercing Will for 15 seconds. The cooldown and windup of Heretic's Sutra scale on your Willpower investment, but the scaling is largely negligible.

### Sin Stacker `[Rare]`
- **설명**: Your All The Dead Gods' duration is now based on how many stacks of antiheal you already have on your opponent, increase your PvE Heal Boost to 10% as well. | **요구조건**: `{'stats': {'Willpower': 90}, 'talents': ['All the Dead Gods']}`
- **추가 정보**: Each stack of any anti-heal increases the duration of subsequent anti-heal stacks by 1 second. For example, your first hit will apply anti-heal for 8 seconds, and your next hit will apply 9 seconds of anti-heal, and so on. Each stack of anti-heal has an independent duration, decaying independently of each other.

### Brick Wall `[Advanced]`
- **설명**: You refuse. You cannot be knocked off your feet until you are knocked completely Unconscious. Also reduces the duration of Knockdown. | **요구조건**: `{'stats': {'Willpower': 100, 'Fortitude': 100}, 'talents': ['Perseverance']}`
- **추가 정보**: Grants full immunity to ragdoll. The knockdown duration reduction scales on your combined Fortitude and Willpower investment, being fully negated if you have 100 points invested into each attribute.

### Not a Scratch `[Advanced]`
- **설명**: You don't show any signs of damage | **요구조건**: `{'stats': {'Willpower': 100, 'Fortitude': 20}}`
- **추가 정보**: Your clothing no longer gets blood splotches and you no longer play low health animations at low health. Your outfit no longer tears when your armor durability is low. Rhythm users can no longer see your health. If you have less than 100 Willpower, your character has a chance to scream in agony upon taking damage.

### Peripheral Vision `[Rare]`
- **설명**: Your glare now ignores if your opponent is facing you. | **요구조건**: `{'stats': {'Willpower': 40}, 'mantras': ['Glare']}`

### Bottom Freeze `[Common]`
- **설명**: Hitting chilled enemies with Ice Projectiles while they are on ice freezes them to the ground. | **요구조건**: `{'stats': {'Frostdraw': 25}, 'mantras': ['Ice Daggers']}`
- **추가 정보**: Prevents you from rotating your character and moving around overall. Taking damage from any source will end Bottom Freeze early.

### Cryonis `[Common]`
- **설명**: All ice spells casted ontop of ice cost less Ether. | **요구조건**: `{'stats': {'Frostdraw': 40}}`
- **추가 정보**: Reduces the Ether cost of Frostdraw Mantras by 40% when standing on ice.

### Frost Buster `[Common]`
- **설명**: Greatsword Criticals and Greathammer Criticals now leave a place Ice below the path they carve. | **요구조건**: `{'stats': {'Heavy Weapon': 15, 'Frostdraw': 45}}`
- **추가 정보**: On critical, create three moderately large ice patches in a linear path in front of yourself. These patches last 1 minute 30 seconds. Despite what the Talent description states, Greathammers do not proc Frost Buster but Greataxes do. Greatcannons do not proc Frost Buster either.

### Frozen Anchor `[Common]`
- **설명**: Apply bottom freeze and chill to your opponent whenever you land a flourish, uppercut, or crit. | **요구조건**: `{'stats': {'Weapon': 100, 'Frostdraw': 100}}`
- **추가 정보**: Bottom Freeze will be removed if the target takes damage from any source. This makes this Talent extremely ineffective on multihit criticals. The Chill applied from this Talent lasts 12 seconds. 10 second cooldown.

### Frostbite `[Common]`
- **설명**: Enemies can no longer heal when Chilled by you. PvE enemies also net you 5% more Heal Boost when Chilled. | **요구조건**: `{'stats': {'Frostdraw': 25}}`

### Frozen Pin-Cushion `[Rare]`
- **설명**: Your Ice Daggers now apply Frozen. | **요구조건**: `{'stats': {'Frostdraw': 60}, 'mantras': ['Ice Daggers']}`
- **추가 정보**: Instantly detonates crystals if you have Crystallization Path.

### Saint Jay `[Rare]`
- **설명**: When a Chilled enemy receives a heal, it's nullified and 60% of the healing is redirected to you. While this is active and they are on ice your rate of healing is increased, raise your PvE Heal Boost to 10% as well. | **요구조건**: `{'talents': ['Frostbite']}`
- **추가 정보**: When a Chilled enemy receives a heal, it's nullified and 60% of the healing is redirected to you. While this is active and they are on ice your rate of healing is increased, raise your PvE Heal Boost to 10% as well.

### Union Card `[Origin]`
- **설명**: A card representing your membership in the Ignition Union. Entitles you to speedier experience gain from Dungeons and Jobs, though the fees will slightly reduce your experience gain outside of these. | **요구조건**: `{'origin': 'Ignition Delver'}`
- **추가 정보**: Gain increased EXP gain from Jobs and Dungeons, but reduced EXP gain from any other content.

### Union Pager `[Origin]`
- **설명**: Check up on job listings remotely. | **요구조건**: `{'origin': 'Ignition Delver'}`
- **추가 정보**: Grants a Talent tool that acts as a remote-access Job Board, allowing you to pick up jobs from any location.

### Union Hook `[Quest]`
- **설명**: You can now make use of the Ignition Union hooks to ascend or descend. | **요구조건**: `{'or': [{'quests': ['"Save Epsi in the entrance of Firfire then speak to Alpha']}, {'origin': 'Ignition Delver'}]}`

### Agitating Spark `[Common]`
- **설명**: Applying Burning to enemies spreads it to anyone nearby. Including yourself. | **요구조건**: `{'stats': {'Flamecharm': 40}}`
- **추가 정보**: On proc, a small orange particle will trail between the burning target you hit and other targets nearby, setting them on fire and granting Emperor Flame stacks. Agitating Spark bypasses block and parry. Agitating Spark procs from self damage do not apply burn. 1 second cooldown.

### Immolation `[Common]`
- **설명**: Fire spells cost 70% less while on fire. If you hit someone while on fire, apply fire damage. You take 50% less damage from self-inflicted flames. | **요구조건**: `{'stats': {'Flamecharm': 40}, 'talents': ['Agitating Spark']}`
- **추가 정보**: "Self-Inflicted flames" include Flame Within, Agitating Spark you spread and environmental burns created by you. "Apply fire damage" applies the burn status effect instead of adding Flamecharm damage. This applies burn regardless of Flamecharm path. Instead, all instances of Physical damage, and all attacks that have the slash (blood particle) fx on hit will proc Immolation, applying burn.

### Phoenix Flames `[Advanced]`
- **설명**: Any time you would burn to death, you instead rise again with 50% of your health restored. Has a 60 second cooldown. | **요구조건**: `{'talents': ['Agitating Spark', 'Immolation']}`
- **추가 정보**: Healing scales on your Flamecharm investment; heals 25% health at 0 Flamecharm and scales up to 50% health at 75 Flamecharm, gaining 0.33% healing per point in Flamecharm. If you used Flame Within while knocked to proc Phoenix Flames, then the healing received will be halved.

### Corpse Explosion `[Common]`
- **설명**: Bodies that you burn to death immediately explode, dealing massive damage. Your fires will incinerate unconscious targets much faster. | **요구조건**: `{'stats': {'Flamecharm': 60}, 'talents': ['Agitating Spark']}`
- **추가 정보**: Executing targets by burning them takes 3.5 seconds instead of 7. The explosion does not work.

### Pleeksty's Faith `[Common]`
- **설명**: When on fire, automatically quench flames at the cost of some ether. | **요구조건**: `{'stats': {'Flamecharm': 25, 'Willpower': 15, 'Charisma': 15}}`
- **추가 정보**: Consumes 20 Ether on proc. Does not proc on self-inflicted flames.

### Pleeksty's Will `[Quest]`
- **설명**: You gain significantly more ether from consuming elemental ingredients. | **요구조건**: `{'or': [{'stats': {'Flamecharm': 40}}, {'stats': {'Charisma': 50}}, {'quests': ["Ploom's Embers"]}]}`
- **추가 정보**: Consuming Gale Stones, Heartstars, Dying Embers, Spark Glands, and Frigid Prisms gives significantly more Ether.

### Ad Astra `[Innate]`
- **설명**: Return Home | **요구조건**: `{'aspect': 'Lightborn'}`
- **추가 정보**: Grants a Talent tool that allows you to travel to and from The Floating Keep.

### Chitin `[Innate]`
- **설명**: You have a layer of Natural Armor that replenishes when you rest | **요구조건**: `{'aspect': 'Vesperian'}`
- **추가 정보**: Grants 5% physical damage reduction in the form of Natural Armor. This stacks multiplicatively with Exoskeleton. Increases Exoskeleton's durability by 200.

### Deepfolk `[Innate]`
- **설명**: The secrets of the Deep are easier for you to unravel. Your mind is sturdier against its effects, as well as using less Knowledge in Knowledge exchanges. | **요구조건**: `{'aspect': 'Ganymede'}`
- **추가 정보**: Increases Sanity gain by 1.2x. Deep Shrine Knowledge cost is reduced by 1 (this cannot go below 1).

### Feathered Glider `[Innate]`
- **설명**: As a show of independence when they come of age, Tirans will strike out on their own with just their hand-crafted glider, gliding down from the mountain peaks where they make their homes. You take 10% less fall damage. | **요구조건**: `{'aspect': 'Tiran'}`
- **추가 정보**: Provides a Glider with infinite durability. The color of this Glider is dependent on your aspect variant, but it can be dyed.

### Echolocator `[Innate]`
- **설명**: Your highly tuned hearing helps you navigate, seeing better in the dark and sensing potential threats. | **요구조건**: `{'aspect': 'Kiron'}`
- **추가 정보**: Pings the location of nearby players who unsheathe their weapons (even through Tacet and Lowstride) and event spawns.

### Loyalty `[Innate]`
- **설명**: Your bond with your allies is strong enough to reduce damage between you. | **요구조건**: `{'aspect': 'Canor'}`
- **추가 정보**: Allies take 35% less damage from you and deal 35% less damage to you. This stacks multiplicatively with Give and Take.

### Mark of Jurik `[Innate]`
- **설명**: Mark of Jurik, the Moonseye. A beacon of calm, those in your presence are resistant to insanity. | **요구조건**: `{'aspect': 'Capra'}`
- **추가 정보**: Gain a tool that lowers the sanity drain of nearby players. Also buffs affected players' HP regen and slightly buffs their food & thirst replenishment from consuming food and their blood regen. 4m CD. These buffs last 1 minute, the HP regen is 15% of their total HP over that one minute period, healing 0.25% HP per second. Also buffs non allies. Does not require you to be resting at a campfire.

### Mark of Ku `[Innate]`
- **설명**: Mark of Ku, the Mother. Improves the rest of those in your presence. | **요구조건**: `{'aspect': 'Capra'}`
- **추가 정보**: Gain a tool that buffs the blood regen of nearby players. Also buffs the affected players' HP regen and slightly buffs their sanity and their food & thirst replenishment from consuming food. 3m 30s CD. These buffs last 1 minute, the HP regen is 15% of their total HP over that one minute period, healing 0.25% HP per second. Also buffs non allies. Can only be used while you are resting on a campfire.

### Mark of Nemit `[Innate]`
- **설명**: Mark of Nemit, the First Beast. Food consumed in your presence is more nourishing. | **요구조건**: `{'aspect': 'Capra'}`
- **추가 정보**: Gain a tool that buffs the food and thirst replenishment of nearby players. Also buffs the affected players' HP regen and slightly buffs their blood regen and sanity. 3m 30s CD. These buffs last 1 minute, the HP regen is 15% of their total HP over that one minute period, healing 0.25% HP per second. Also buffs non allies. Can only be used while you are resting on a campfire.

### Maudet `[Innate]`
- **설명**: Your understanding of your destiny is such that learning new things often comes naturally to you. People appreciate your diplomatic ways of speaking. | **요구조건**: `{'aspect': 'Adret'}`
- **추가 정보**: Gain 3 free investment points to invest every time you level up. This stacks with Autodidact. Your starting reputation with all factions is higher.

### Molt `[Innate]`
- **설명**: Ailments and blessings alike fade away more quickly. | **요구조건**: `{'aspect': 'Etrean'}`
- **추가 정보**: The duration of Chill, Suffocation, and all potion effects is reduced.

### Mothwing Dust `[Innate]`
- **설명**: You release Mothwing Dust when others are the first to strike, granting you vision of your attacker. Your antennae improve your peripheral senses, narrowing the angle at which you can be backstabbed. | **요구조건**: `{'aspect': 'Chrysid'}`
- **추가 정보**: Upon being hit at the start of combat, cover your opponent in Mothwing Dust, applying a red highlight on your opponent for 10 seconds. This highlight can be seen through walls.

### Navae's Guidance `[Innate]`
- **설명**: Navae's star guides your path, showing you the way forward. Right-clicking on maps sets a Waymarker which can be followed. You are less prone to starvation. | **요구조건**: `{'aspect': 'Gremor'}`
- **추가 정보**: Receive a compass, displayed at the top of your screen, which points East. Right clicking on the map will place a waypoint or change the location of a pre-existing one. Waymarkers can be seen both in the physical world and on the map. The passive hunger loss is reduced.

### Nightchild `[Innate]`
- **설명**: Relying on your instincts, you are naturally more stealthy. You are more nimble on wooden surfaces. | **요구조건**: `{'aspect': 'Felinor'}`
- **추가 정보**: Multiplies all stealth gained by 1.2x. Gain +20% Stealth on spawn.

### Seaborne `[Innate]`
- **설명**: You have a keen understanding of ships and their maintenance. | **요구조건**: `{'aspect': 'Celtor'}`
- **추가 정보**: Ship purchase price is reduced by 20%, ships turn 20% faster, and have 10% more health. Repairing a ship with a Repair Hammer takes less time.

### Teachings of the Edenkite `[Spec]`
- **설명**: Find your centre. | **요구조건**: `{'aspect': 'Drakkard'}`
- **추가 정보**: Allows you to meditate, emitting a white aura and causing two white orbs to circle your head. Very heavily reduces your hunger and thirst consumption while you passively gain EXP and Attribute EXP and regenerate health at a mediocre rate, which is slightly reduced when in combat.

### Versatile `[Innate]`
- **설명**: You learn how to use new pieces of equipment quicker than others. You can equip things at 3 points lower than the requirement. | **요구조건**: `{'aspect': 'Khan'}`
- **추가 정보**: Reduces the attribute requirements of all equipment and weapon items by 3. This is applied to each requirement individually, meaning you can save upwards of 12 points.

### Backstabber `[Faction]`
- **설명**: Landing a backhit with a light attack causes you to grab your opponent and stab them again, dealing an extra 15 damage. [15 second CD]
 | **요구조건**: `{'stats': {'Agility': 30}, 'objectives': ['Inquisition Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: Deals 20 damage, not 15. You gain a 10% swing speed buff when standing behind targets when this is off cooldown. Has no range limit. Also procs on criticals with the M1 tag. Proccing Backstabber gives the target 3 seconds of Backstabber immunity. Applies daze and ragdolls.

### Executioner's Frenzy `[Faction]`
- **설명**: Landing a light attack while their posture is paused reduces their assassination cooldown by 5 seconds. | **요구조건**: `{'objectives': ['Inquisition Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: This works on Paused Posture caused from Stature Break or Maiming Claws.

### Fatal Stealth `[Faction]`
- **설명**: You deal increased backstab damage to opponents based on how high your stealth stat currently is. | **요구조건**: `{'objectives': ['Inquisition Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: Grants a 0.2% damage buff to attacks that hit your opponent's back for every 1% stealth you have. This only works on stealth gained from Equipment or Outfit sources. Felinor's innate stealth multiplier has no effect on this. This does not work on assassinations.

### Flanking Maneuvers `[Faction]`
- **설명**: Enemies you assassinate take more PEN from your squadmates in your party. | **요구조건**: `{'objectives': ['Inquisition Division'], 'origin': 'Authority Ensign'}`

### Stature Break `[Faction]`
- **설명**: Landing a backstab of any kind disables posture for 4 seconds. [8 second CD] | **요구조건**: `{'objectives': ['Inquisition Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: While their posture is paused, your opponent cannot restore posture by parrying, spitting, passive posture restoration, or through Steady Nerves. All other forms of posture restoration ignore this effect entirely.

### Tacet Minimization `[Faction]`
- **설명**: Focus your Tacet even further, allowing the radius at which you get spotted to become smaller temporarily. | **요구조건**: `{'objectives': ['Inquisition Division'], 'origin': 'Authority Ensign', 'murmur': 'Tacet'}`
- **추가 정보**: Grants a Talent tool that massively reduces the size of your Tacet bubble on use.

### Critical Engine `[Common]`
- **설명**: You gain the ability to use Deep Gems on your critical attack. Hold out the Deep Gem you wish to apply to your crit then use the tool to enhance your critical. | **요구조건**: `{'stats': {'Weapon': 30, 'Intelligence': 90}}`
- **추가 정보**: Hold out the Deep Gem you wish to equip to your weapon and click to apply it, similar to equipping a Deep Gem to a Mantra. This does not consume the Deep Gem on use. Blue Gems have a unique interaction with this Talent, granting Ether back based on scaled damage dealt.

### Ironsing Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Ironsing to its fullest. | **요구조건**: `{'stats': {'Ironsing': 75}, 'talents': ['Master Ironsinger'], 'slay': 'Any humanoid boss'}`
- **추가 정보**: Removes the 75 investment cap on the Ironsing Attribute. This Talent will be removed if you do not meet its stat requirements.

### Ironsinger `[Common]`
- **설명**: Grants you the ability to command Metal as an Ironsinger. Press X to Pull on Metal Rods. | **요구조건**: `{'stats': {'Ironsing': 1}}`
- **추가 정보**: Ironsing mantras apply stacks of Metal Rods on targets. Pressing [X] will pull affected towards you, with the strength of the pull depending on the amount of Metal Rods present. You cannot apply more than 5 Metal Rods to one target, unless you have one of the Rending Needle Talents.

### Adept Ironsinger `[Common]`
- **설명**: You can now obtain 1-star Ironsinger mantras. | **요구조건**: `{'stats': {'Ironsing': 20}, 'talents': ['Ironsinger']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Expert Ironsinger `[Common]`
- **설명**: You can now obtain 2-star Ironsinger mantras. | **요구조건**: `{'stats': {'Ironsing': 30}, 'talents': ['Adept Ironsinger']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Master Ironsinger `[Common]`
- **설명**: You can now obtain 3-star Ironsinger mantras. | **요구조건**: `{'stats': {'Ironsing': 50}, 'talents': ['Expert Ironsinger']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Alloyblood `[Advanced]`
- **설명**: You don't bleed like others do. Bleed damage reduced by 30%. Blood loss is reduced by 75%. | **요구조건**: `{'stats': {'Ironsing': 100}}`
- **추가 정보**: The effects of Alloyblood scale linearly with Ironsing investment, losing 0.3% bleed damage reduction and 0.75% blood loss damage reduction for every point in Ironsing below 100. Blood loss reduction is less effective if you are using the Curse of the No Life King Enchantment and stacks multiplicatively with Cauterized Wounds. The blood loss reduction does not affect blood drain effects like casting or being hit by Bloodrend Mantras, blood drain potions, and the blood loss Corrupt Resonance downside.

### Heavy Shoulders `[Common]`
- **설명**: If your opponent has 3 or more rods, their dodges are slower. | **요구조건**: `{'stats': {'Ironsing': 55}}`
- **추가 정보**: Reduces roll distance by 10%.

### Laced Traps `[Common]`
- **설명**: People hit by your 'Caltrops' cannot jump and are slowed for a small duration, while also applying Sluggish to PvE enemies for a few seconds. | **요구조건**: `{'stats': {'Ironsing': 45}, 'mantras': ['Caltrops']}`
- **추가 정보**: Landing a Caltrop slows down your opponent and disables their ability to jump for 1.1 seconds. This effect refreshes if the victim gets hit by another Caltrop.

### Metal Shackles `[Common]`
- **설명**: Guardbreaking an opponent prevents them from receiving speed boost for 5 seconds, while PvE opponents will be Sluggish for 12 seconds. | **요구조건**: `{'stats': {'Ironsing': 40, 'Strength': 15}}`

### Piercing Metal `[Common]`
- **설명**: Deal additional armor damage to enemies per metal rod affecting them. | **요구조건**: `{'stats': {'Power': 13, 'Ironsing': 60}}`
- **추가 정보**: Each rod increases armor damage dealt through weapon attacks and Mantras by 5%. This does not affect armor drain effects such as the Metal enchantment.

### Thornmail `[Common]`
- **설명**: Getting flourished applies a metal rod on your attacker. | **요구조건**: `{'stats': {'Ironsing': 45}}`

### Willpower Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your willpower to its fullest. | **요구조건**: `{'stats': {'Willpower': 75}, 'quests': ['Speak to Akira in the Depths then speak to him again after he moves to Castle Light']}`
- **추가 정보**: Removes the 75 investment cap on the Willpower Attribute. The stat requirements to obtain this Talent will be increased to 77 or 78 if your Aspect has increased Willpower on spawn, though this limitation will be removed if you have the Multifaceted Echo Unlock. The quest requirement for this Talent will be removed if you've obtained it previously on your account.

### Grand Skewer `[Rare]`
- **설명**: Your Grand Javelin now carries opponents through the air. | **요구조건**: `{'stats': {'Thundercall': 60}, 'mantras': ['Grand Javelin']}`
- **추가 정보**: Press [F] during Grand Javelin's windup to activate this effect. This does not work in Layer 1.

### Oath: Jetstriker `[Oath]`
- **설명**: You vow to flow with the Song itself, drifting across where the trails may take you. If the Song permeates everything, then let it be your conduit, and you its master. | **요구조건**: `{'stats': {'Agility': 50}, 'objectives': ['Beat Alirian in a race.']}`
- **추가 정보**: Gain Momentum by sprinting. At maximum Momentum, your Jetstriker Mantras deal 20% more damage.

### Acceleration Points `[Oath]`
- **설명**: Striking an opponent in the back with mobility mantras or Basic Attacks now steals and grants additional momentum. | **요구조건**: `{'talents': ['Oath: Jetstriker']}`

### Decisive Winds `[Oath]`
- **설명**: When damage below 50% health, don an aura of Decisive Winds for 10s. | **요구조건**: `{'talents': ['Oath: Jetstriker']}`
- **추가 정보**: The Decisive Winds status effect grants a 25% speed boost as long as you are within 20 studs of the target who initiated this effect. This procs through block, parry, and dodge, but not on self damage. 30 second cooldown.

### Jetstream Pursuit `[Oath]`
- **설명**: Upon a successful flourish, teleport to the opponent when they stop moving. Receive a significant boost of momentum. | **요구조건**: `{'talents': ['Oath: Jetstriker']}`

### Rush of Ancients `[Oath]`
- **설명**: Dashing at maximum sprint momentum makes you one with the wind itself. | **요구조건**: `{'talents': ['Oath: Jetstriker']}`
- **추가 정보**: Extends your dash distance and makes you invisible for a very brief duration when you dash.

### Stratos Step `[Oath]`
- **설명**: Holding space while climbing will now let your perform Stratos Steps to get even higher. | **요구조건**: `{'talents': ['Oath: Jetstriker']}`
- **추가 정보**: Stratos Steps will only proc twice before going on a cooldown. Said cooldown applies to individual steps. Additionally, Stratos Step consumes Ether per step.

### Electrify `[Common]`
- **설명**: Shock yourself and apply Amped for 15s. Can be used while Carried to escape. | **요구조건**: `{'stats': {'Thundercall': 25}}`
- **추가 정보**: If used while not being carried, this deals 5% of your current health as self damage on proc. Additionally, you will gain the Amped status effect for 15 seconds, increasing your weapon damage by 10% and allowing your weapon attacks to apply Shock on hit. However, incoming damage will be increased by 10%. 1 minute cooldown.

### Amplified Reflexes `[Common]`
- **설명**: Amped now grants enhanced speed and parkour. | **요구조건**: `{'stats': {'Thundercall': 35}, 'talents': ['Electrify']}`
- **추가 정보**: While Amped, your walk speed will be increased by 50% and your climb height will be increased by 15%. You also gain a slight sprint speed buff.

### Amplified Rage `[Common]`
- **설명**: Amped now grants you an additional +10% weapon damage. Also self-damage and cooldown by 3x. | **요구조건**: `{'stats': {'Thundercall': 35}, 'talents': ['Electrify']}`
- **추가 정보**: Increases Amped's damage buff from 10% to 20%. The final sentence in this Talent's description is lying; it does not increase Electrify's cooldown, nor its self damage.

### Jus Karita `[Quest]`
- **설명**: Adopt the kick-based fighting style of the Justicars. | **요구조건**: `{'or': [{'stats': {'Power': 5, 'Light Weapon': 40}, 'objectives': ['Talk to Polis']}, {'objectives': ['Spawn in with the Jus Karita Fist style'], 'or': [{'origin': 2690}]}]}`
- **추가 정보**: Allows you to use the Jus Karita fist style.

### Justicar's Prowess `[Common]`
- **설명**: Jus Karita gains +30% posture damage against other fist styles. | **요구조건**: `{'talents': ['Jus Karita']}`
- **추가 정보**: Gain +30% posture damage on weapon attacks against opponents using Way of Navae, Fang and Coil, Imperium Kata, Untrained Fist, or Legion Kata.

### Justicar's Renewal `[Common]`
- **설명**: Hitting an opponent with your Jus Karita critical resets the cooldown. (Cooldown of 10 seconds). | **요구조건**: `{'talents': ['Jus Karita']}`
- **추가 정보**: Landing Jus Karita's critical attack will reset its cooldown. This has a 10 second cooldown. Also procs if Jus Karita's critical is blocked or parried.

### Flying Swiftkick `[Common]`
- **설명**: Hitting a Jus Karita critical attack while Swiftkick Prodigy is active will greatly slow your enemy, and consume your speed boost. | **요구조건**: `{'talents': ['Jus Karita', 'Swiftkick Prodigy']}`

### Kickstart `[Common]`
- **설명**: Play the resurrector. Use your lightning to defibrillate your allies on the battlefield. | **요구조건**: `{'stats': {'Thundercall': 50}, 'or': [{'stats': {'Fortitude': 40}}, {'stats': {'Charisma': 40}}]}`
- **추가 정보**: Heals the person for 10% of their maximum health if you successfully resurrect them. Kickstart consumes 5% of your Ether on use, and then another 20% if the Kickstart was successful. Kickstart has a 3 second long animation, in which you cannot act. This can be used on players using Cap Artist. Despite the description stating "allies," this can be used on non-allies and humanoid NPCs.

### Blade's Edge `[Common]`
- **설명**: [Spears] Damage dealt with the tip of the spear is increased by 10% | **요구조건**: `{'stats': {'Medium Weapon': 30}, 'weaponType': 'Spear'}`
- **추가 정보**: The "tip of the spear" is the end of your weapon's range.

### Defensive Sweep `[Common]`
- **설명**: [Spears] Posture breaking an opponent grants you +50% PEN for 3 seconds. | **요구조건**: `{'stats': {'Medium Weapon': 50}, 'weaponType': 'Spear'}`
- **추가 정보**: This does not bypass the PEN cap. 14 second cooldown.

### Driving Impact `[Common]`
- **설명**: [Spears] The first hit of your Spear's Critical Attack will deal greatly increased posture damage. Subsequent hits will do reduced posture damage. | **요구조건**: `{'stats': {'Medium Weapon': 30}, 'weaponType': 'Spear'}`
- **추가 정보**: The first hit of your default spear critical will deal double the posture damage. The second hit of your default spear critical will not deal posture damage.

### Lancer's Impale `[Common]`
- **설명**: [Spears] Hitting an enemy after a perfect dodge makes your next attack deal 30% bleed damage. If that attack would already bleed, it adds +10% chip damage instead. | **요구조건**: `{'stats': {'Medium Weapon': 30}, 'weaponType': 'Spear'}`

### Hoplite `[Common]`
- **설명**: Posture damage is reduced by 15% when wielding a spear and standing still. | **요구조건**: `{'stats': {'Fortitude': 15}, 'weaponType': 'Spear'}`

### Eruption Path: Lava Serpent `[Common]`
- **설명**: Your fire abilities no longer proc burn and instead proc an eruption under the enemies feet. | **요구조건**: `{'stats': {'Flamecharm': 40}}`
- **추가 정보**: Eruptions have a base damage of 15 with 5 Flamecharm scaling. Eruptions have a 3s proc cooldown. You can still apply burn via Immolation, Flash Point, and Agitating Spark.

### Empowered Eruption `[Common]`
- **설명**: Your next Eruption after landing a critical is Empowered with +50% range and damage. 10s cooldown. | **요구조건**: `{'stats': {'Flamecharm': 50}, 'talents': ['Eruption Path: Lava Serpent']}`

### Flash Point `[Common]`
- **설명**: Block breaking an opponent causes your Eruptions to be Empowered for the next 10s. Block breaking an opponent with a Fire Mantra procs Burning. | **요구조건**: `{'stats': {'Flamecharm': 55}, 'talents': ['Eruption Path: Lava Serpent']}`
- **추가 정보**: 45 second cooldown on the Empowered Eruption effect.

### The Floor is Lava `[Advanced]`
- **설명**: Your Eruptions leave lethal pools of lava beneath them. Don't fall in. | **요구조건**: `{'stats': {'Flamecharm': 100}, 'talents': ['Eruption Path: Lava Serpent']}`
- **추가 정보**: The duration and damage of the lava pools scale on your Flamecharm investment.

### Callout `[Common]`
- **설명**: You can mark objects or enemies by pressing Z, which will mark them for all nearby allies. | **요구조건**: `{'stats': {'Charisma': 20}}`

### Spotter `[Common]`
- **설명**: Marking enemies while in Rhythm will now indicate their health status to your allies. | **요구조건**: `{'or': [{'stats': {'Charisma': 40}, 'talents': ['Murmur: Rhythm']}, {'talents': ['Oath: Soulbreaker']}]}`
- **추가 정보**: Using Callout while in Rhythm will showcase the health value of the target to your allies.

### Observation `[Rare]`
- **설명**: Dodge frames are larger if you cancel your roll immediately. | **요구조건**: `{'stats': {'Agility': 20}}`
- **추가 정보**: Cancelling your roll quickly will keep your dodge for as active as a full roll, giving you an additional ~0.1s immunity.

### Safety Dance `[Rare]`
- **설명**: Your base dodge frames are increased by 0.05s. | **요구조건**: `{'stats': {'Agility': 20}}`
- **추가 정보**: Dodge IFrames increased from 0.3s to 0.35s.

### Air Pressure `[Common]`
- **설명**: Dodging an attack or hitting an enemy's block will transform your next dash into a Gale Dash. Gale Dashes carry you further than regular dashes and have extended iframes, but will clear immediately should you initiate an attack. | **요구조건**: `{'stats': {'Agility': 20, 'Galebreathe': 50}}`

### Cyclone Blade `[Common]`
- **설명**: After a successful Gale Dash you wrap your weapon in wind, causing your next Light attack to do +15% damage as bleed and have +10% chip damage. | **요구조건**: `{'stats': {'Agility': 30, 'Galebreathe': 55}, 'talents': ['Air Pressure']}`
- **추가 정보**: Lasts for 3 seconds with no cooldown. Phantom Step dashes will also proc this effect. Despite stating "Light Attack", this Talent also procs on weapon criticals.

### Pressure Break `[Common]`
- **설명**: Breaking an enemy's posture will cause them to take intense wind pressure, increasing the attack's damage by +15% and flinging the enemy backwards. | **요구조건**: `{'stats': {'Galebreathe': 65}, 'talents': ['Air Pressure'], 'or': [{'stats': {'Agility': 30}}, {'stats': {'Strength': 30}}]}`

### Wind Step `[Common]`
- **설명**: Create a step of wind below you when jumping in the air. Jumping while sliding down a slope or off a cliff launches you forwards. | **요구조건**: `{'stats': {'Galebreathe': 40}}`
- **추가 정보**: Jump while airborne to double jump, leaving behind a wind pad that other players can also use. Alternatively, jumping while sliding down a slope will perform a Gale Leap that propels you forwards. While in combat, this ability cost Ether to use.

### Scorched Peak `[Common]`
- **설명**: Blockbreaking an enemy on fire or with a fire mantra causes them to be struck by lightning. | **요구조건**: `{'stats': {'Thundercall': 50, 'Flamecharm': 25}}`
- **추가 정보**: Deals 10 Thundercall damage on hit. "On fire" refers to the Burn status effect. This can proc Grounding Bolt.

### Comeback Kid `[Common]`
- **설명**: When waking up from being knocked you are unable to be knocked down for 5 seconds. (120 second cooldown) | **요구조건**: `{'stats': {'Power': 8}}`
- **추가 정보**: 2 minute cooldown.

### Last Resort `[Common]`
- **설명**: Deal +5% more damage when your health is below 25%. | **요구조건**: `{'stats': {'Willpower': 35}}`

### The Eleventh Hour `[Common]`
- **설명**: When below 15% health your mantras require no ether to cast for 11 seconds. | **요구조건**: `{'stats': {'Willpower': 35}}`
- **추가 정보**: Lasts 30 seconds with a 90 second cooldown.

### Oath: Linkstrider `[Oath]`
- **설명**: You vow to give up your own life for the sake of others. Stepping out of the fray, you become a foundation of your allies' strength. | **요구조건**: `{'objectives': ['Entropy Catalyst']}`

### Entropy Link `[Oath]`
- **설명**: The world is broken, linked by fragile webs. Traverse the path by stating your destination amidst the flame. | **요구조건**: `{'talents': ['Oath: Linkstrider'], 'objectives': ['Linkstrider Progression']}`
- **추가 정보**: You are able to fast travel to certain places while resting at a campfire. Locations are unlocked by interacting with special meteorites that are scattered around the map. By sitting at a campfire and typing out the name of the desired meteorite, you will be transported directly to it.

### Symbiotic Link `[Oath]`
- **설명**: Activate by pressing X while hovering over an ally or enemy. The Links are destroyed when you receive damage from a non-ally, you stray too far or you activate it again. Only one cord of each type may exist at once, links give a 3 second warning in break range, in the warning phase, they can't be broken. | **요구조건**: `{'talents': ['Oath: Linkstrider'], 'objectives': ['Linkstrider Progression']}`
- **추가 정보**: Blue Cords (Allies) gain a speed boost, 20% damage resistance, and a 5% damage increase. Red Cords (Enemies) gain a minor speed debuff. Allows you to passively see the health bars of your allies.

### Mark of the Lone Warrior `[Origin]`
- **설명**: Progress much faster when progressing alone. Gain a damage boost when facing threats alone and also when outnumbered. | **요구조건**: `{'objectives': ['Complete the Trial of One'], 'origin': 'Lone Warrior'}`
- **추가 정보**: Gain an experience gain multiplier if nobody else has combat tagged the enemy. Gain a 5% damage buff against enemies who have combat tagged you, or enemies you've combat tagged if the opponent has less than or an equal amount of combat tags as you.

### Silencer's Song `[Common]`
- **설명**: Silencer's Blade now procs on your mantras. | **요구조건**: `{'stats': {'Weapon': 100, 'Galebreathe': 100}, 'talents': ["Silencer's Blade"]}`
- **추가 정보**: Landing any Mantra on a suffocated target creates a new stack of suffocation that lasts 5 seconds. Additionally, you gain a 22.5% speed boost for 3 seconds.

### Old Habits Die Hard `[Common]`
- **설명**: Blocking an attack with your lingering block frames after failing a parry will cause the attack to deal 15% less posture damage. | **요구조건**: `{'stats': {'Willpower': 20}}`

### Thresher Claws `[Rare]`
- **설명**: Grants +5% Weapon PEN. | **요구조건**: `{'stats': {'Power': 13}}`

### Leg Shot `[Rare]`
- **설명**: [Rifles] Landing your critical slows your enemy for a bit while making PvE enemies Sluggish, and also disables any speed boosts they get for the next 10 seconds. | **요구조건**: `{'stats': {'Medium Weapon': 80}, 'weaponType': 'Rifle'}`

### Stock Bash `[Common]`
- **설명**: [Rifles] Your running attacks now apply a brief amount of daze and Stagger PvE enemies. | **요구조건**: `{'stats': {'Medium Weapon': 55, 'Strength': 25}, 'weaponType': 'Rifle'}`
- **추가 정보**: Applies daze for one second.

### Tactical Reload `[Rare]`
- **설명**: [Rifles] Activate to make your rifle shoot bullets for 15 seconds. | **요구조건**: `{'stats': {'Medium Weapon': 95}, 'weaponType': 'Rifle'}`
- **추가 정보**: Upon activating the Talent tool, your rifle will gain the ability to fire Bullets for 15 seconds. 90 second cooldown. Does not work on Rifle Spear.

### Impervious Slumber `[Rare]`
- **설명**: Getting hit while Unconscious no longer resets your time Unconscious. | **요구조건**: `{'stats': {'Fortitude': 35}}`

### Breathing Exercise `[Common]`
- **설명**: Your sanity recovers more quickly once out of terrifying situations. | **요구조건**: `{'stats': {'Willpower': 5}}`
- **추가 정보**: Your passive sanity regen is increased by 50%.

### Conquer your Fears `[Common]`
- **설명**: Killing the beings of the deep replenishes your sanity somewhat. When an Ally grips an enemy nearby to you, you regain Sanity. | **요구조건**: `{'stats': {'Willpower': 10}, 'talents': ['Breathing Exercise']}`
- **추가 정보**: Recover Sanity when killing monsters in the Depths, with the Sanity restored depending on how strong the monster is. Gain Sanity whenever a nearby ally executes a humanoid target.

### Disbelief `[Common]`
- **설명**: Reduces the duration of illusions cast on you by 30%. Halves the duration of the Charmed status on you. | **요구조건**: `{'stats': {'Willpower': 25}}`
- **추가 정보**: All Visionshaper clones have a 30% less duration when cast on you. Halves the duration of Charmed.

### Intuitive Repairs `[Common]`
- **설명**: Your 'Iron Skin' repairs armor while it's active. | **요구조건**: `{'stats': {'Ironsing': 25}, 'mantras': ['Iron Skin']}`
- **추가 정보**: Iron Skin regenerates your armor and Natural Armor while its active.

### Metal Absorption `[Common]`
- **설명**: Your 'Iron Hug' also absorbs armor from the enemy. | **요구조건**: `{'stats': {'Ironsing': 30}, 'mantras': ['Iron Hug']}`
- **추가 정보**: Iron Hug will steal 10% of your opponent's current armor durability and siphon it back to yourself.

### Metal Eater `[Common]`
- **설명**: When you have no ether, consume Armor durability to cast your Ironsing mantras. | **요구조건**: `{'stats': {'Ironsing': 50}}`
- **추가 정보**: Consumes 30% of your maximum armor on proc, regardless of the Ether cost of the Mantra.

### Metal Thief `[Common]`
- **설명**: Pulling an opponent absorbs a portion of their current Armor durability. | **요구조건**: `{'stats': {'Ironsing': 50}}`
- **추가 정보**: Steals 2% of your opponent's current armor durability per rod.

### Polished Armor `[Common]`
- **설명**: You receive 5% less damage when your Armor protects you from an attack and has over 90% durability. This 5% will scale up to 10% less damage at 100 MTL. | **요구조건**: `{'stats': {'Ironsing': 75}}`
- **추가 정보**: The damage reduction of Polished Armor is increased by 0.05% per Ironsing investment, granting 8.75% damage reduction at requirements.

### Chain of Perfection `[Quest]`
- **설명**: You gain stacks of Perfection on hitting mobs with Weapon Attacks or Mantras. Mantras are only worth half a stack. | **요구조건**: `{'stats': {'Power': 1}, 'slay': 'Any boss, while solo and without taking any damage.'}`
- **추가 정보**: Gain a 5% damage buff against PVE enemies per stack of Perfection above 5, capping at +100% damage at 25 stacks. This is treated as a final damage multiplier and it bypasses the damage modifier cap. All stacks of Perfection are lost upon taking any damage, excluding self damage.

### Echoing Lunatic `[Common]`
- **설명**: Your Ardour Scream now inflicts insanity. | **요구조건**: `{'stats': {'Willpower': 55}, 'talents': ['Ardour Scream']}`

### Lose Your Mind `[Rare]`
- **설명**: Deal more damage the more insane you are. Grants +15% damage at maximum insanity. | **요구조건**: `{'stats': {'Strength': 30, 'Fortitude': 30}}`
- **추가 정보**: Starting at 70% Sanity, gain a damage buff that scales non-linearly on your current Sanity percentage.

### Shared Misery `[Common]`
- **설명**: Using a M1/Critical Attack on an enemy while losing sanity causes them to lose sanity. | **요구조건**: `{'stats': {'Willpower': 85}}`
- **추가 정보**: If you are actively losing sanity or have used Heretic's Sutra in the past 15 seconds, remove 3% of the target's maximum sanity, scaled down if you have less than 85 Willpower.

### Charisma Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your charisma to its fullest. | **요구조건**: `{'stats': {'Charisma': 75}, 'quests': ['Diver Apprentice']}`
- **추가 정보**: Removes the 75 investment cap on the Charisma Attribute. The stat requirements to obtain this Talent will be increased to 77 or 78 if your Aspect has increased Charisma on spawn, though this limitation will be removed if you have the Multifaceted Echo Unlock. The quest requirement for this Talent will be removed if you've obtained it previously on your account.

### Murmur: Ardour `[Murmur]`
- **설명**: An application of your Soul Murmur that enables one to channel the murmur into raw strength. Press H. | **요구조건**: `{'or': [{'slay': 'Dread Serpent'}, {'slay': 'The Doom of Caeranthil'}, {'objectives': ['Talk with the Old Stranger']}, {'talents': ['Oath: Soulbreaker']}]}`
- **추가 정보**: Drains Ether while active, with the Ether drain scaling inversely with your level and being entirely negated at Power 20. Ardour automatically deactivates if you run out of Ether. Increases the posture damage of M1s and critical attacks with the M1 tag by 20%. Reduces incoming posture damage by 15%. Additionally applies a +15% damage buff to M1s and critical with the M1 tag that guard break.

### Ardour Scream `[Common]`
- **설명**: Amplify your shout into a scream using Ardour, dominating weaker foes, Victims take 12.5% more damage and 50% more posture damage for 10s. | **요구조건**: `{'or': [{'stats': {'Willpower': 40, 'Strength': 15}, 'talents': ['Murmur: Ardour']}, {'talents': ['Oath: Soulbreaker']}, {'set': 'Broodplate'}]}`
- **추가 정보**: Consumes 100% of your Ether on use. Ardour Scream requires you to have a minimum of 100% Ether to be casted. Having the Soul Infusion Talent will reduce this to a minimum of 40% Ether.  Combat tags opponents hit. Notably, its damage and posture damage buffs are applied on-hit to incoming attacks rather than being a debuff that increases damage/posture damage taken, meaning Ardour Scream is affected by the damage and posture damage modifier caps. Also has a 95-Stud range (245 if Soulbreaker),

### Murmur: Rhythm `[Murmur]`
- **설명**: An application of your Soul Murmur that enables the user to perceive the subtle murmur emanating from all things. Press G while crouched. | **요구조건**: `{'or': [{'objectives': ["Complete Kadrivus Entomolius Auditan's Quest in the Second Layer"]}, {'talents': ['Oath: Soulbreaker']}]}`
- **추가 정보**: Pings all nearby Monsters, NPC’s, and Players, through walls while gray-scaling your screen. Red = Low Health, Yellow = Moderate Health, Grey = Healthy.

### Murmur: Tacet `[Murmur]`
- **설명**: An application of your Soul Murmur that enables the user to suppress their own murmur. Press T while crouched. | **요구조건**: `{'or': [{'stats': {'Charisma': 10}, 'objectives': ['5 Cestis Bounties']}, {'objectives': ['Complete 5 Bounty Hunting Contracts']}, {'talents': ['Oath: Soulbreaker']}]}`
- **추가 정보**: On use, a sphere around your character will be created. To everyone outside of the sphere, you are invisible. The size of the Tacet sphere scales inversely on your level and your stealth stat, becoming smaller the higher your level and the more stealth you have. In PvE you become effectively invisible to enemies at almost any range. Tacet will deactivate if you: stop crouching for 3 seconds, sprint for 1.5 seconds, use any attack, get hit, or use Soulbreaker's Formless ability. Tacet will be disabled during Hell Mode, Diluvian, and Depths Trials.

### Armor Conserver `[Common]`
- **설명**: You lose 15% less armor when hit. | **요구조건**: `{'stats': {'Power': 8}}`
- **추가 정보**: Does not affect Natural Armor from Exoskeleton and Chitin.

### Lightweight `[Common]`
- **설명**: Move faster when your armor runs out of durability.
- **추가 정보**: Grants a +25% movement speed buff. This is not a speed boost, meaning it won't proc any speed boost-reliant Talents.

### Padded Armor `[Common]`
- **설명**: While your armor is broken (or if you have no armor), you take 5% less damage. | **요구조건**: `{'stats': {'Power': 8}}`
- **추가 정보**: The 3% Blunt Armor is multiplicative with other sources of Blunt resistance.

### Steel Scales `[Common]`
- **설명**: You take an additional 5% less damage when your armor is broken. | **요구조건**: `{'stats': {'Power': 8}, 'talents': ['Padded Armor']}`
- **추가 정보**: The 3% Slash Armor is multiplicative with other sources of Slash resistance.

### Captain Etrea `[Common]`
- **설명**: [Fists] Moving while blocking with a shield no longer slows you down. | **요구조건**: `{'stats': {'Strength': 30, 'Fortitude': 20}, 'talents': ['Moving Fortress'], 'weaponType': 'Fist'}`

### Fists of Fortitude `[Rare]`
- **설명**: Fists Every 6 hits with your fists builds up a shield of endurance reducing incoming damage by 15%. 70s CD | **요구조건**: `{'stats': {'Light Weapon': 20, 'Fortitude': 20}, 'weaponType': 'Fists'}`
- **추가 정보**: Lasts 10 seconds then goes on cooldown once the buff ends. You can only gain stacks from M1s or criticals with the M1 tag.

### Way of Navae `[Quest]`
- **설명**: Gain the ability to use fist combat against weapons. Including the ability to block weapons with your hands using Ether. | **요구조건**: `{'objectives': ['Bring a Navaen Hostage to the Eastern Camp Master, Beiruul, or Eastern Nomad Leader.']}`
- **추가 정보**: Allows you to use the Way of Navae fist style.

### Defensive Stance `[Common]`
- **설명**: [Rapier] Gain more parry frames the lower your health is. | **요구조건**: `{'stats': {'Light Weapon': 50}, 'weaponType': 'Rapier'}`

### Duelist's Lunge `[Common]`
- **설명**: [Rapier] Running attacks deal increased posture damage. Upon landing your Critical, your next running attack will have increased range. | **요구조건**: `{'stats': {'Light Weapon': 30}, 'weaponType': 'Rapier'}`
- **추가 정보**: Running attacks with rapiers deal 35% more posture damage. After landing a Critical, the next rapier running attack gains 2 range.

### Frenzied Dance `[Common]`
- **설명**: [Rapier] The more posture you currently have, the more chip and posture damage you deal. | **요구조건**: `{'stats': {'Light Weapon': 50}, 'weaponType': 'Rapier'}`

### Pressure Skewer `[Common]`
- **설명**: [Rapier] Flourishing an enemy causes your M1's to deal additional chip damage, blood loss and makes your hits deal 3 extra true damage until you take damage. | **요구조건**: `{'stats': {'Light Weapon': 40}, 'weaponType': 'Rapier'}`
- **추가 정보**: Increases blood bar damage by 50% and grants +25% Chip damage while active. These bonuses apply to M1s and criticals with the M1 tag.

### Fast Blade `[Common]`
- **설명**: Extend the speed boost you get from successfully parrying an attack. | **요구조건**: `{'stats': {'Agility': 20}}`
- **추가 정보**: Increases the speed boost duration from parrying by 3 seconds.

### Lightspeed Reflexes `[Rare]`
- **설명**: Feinting your Basic Attacks gives a very brief auto-parry window. | **요구조건**: `{'stats': {'Agility': 20, 'Intelligence': 20}}`

### Speed Emission `[Common]`
- **설명**: Gain a slight speed boost after landing a vent | **요구조건**: `{'stats': {'Agility': 25}}`

### Oath: Oathless `[Oath]`
- **설명**: You vow to never be bound to any Oath; to live your life free of restraint. If free will is an illusion, why not make it a convincing one? | **요구조건**: `{'objectives': ["Talk to Cerulean in the cave near Miner's Landing docks, 10 minutes of playtime"]}`
- **추가 정보**: Notably, the Oath Armor given by this Talent is affected by PEN and will be nullified if you run out of armor durability. Additionally, due to how resistances work, Oath attacks that have dual damage typings will ignore your Oath armor.

### All Knowing `[Rare]`
- **설명**: Your prediction now ignores the range requirement to reflect attacks. | **요구조건**: `{'stats': {'Intelligence': 60}, 'mantras': ['Prediction']}`

### Intelligence Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Intelligence to its fullest. | **요구조건**: `{'stats': {'Intelligence': 75}, 'objectives': ['Complete the Birdcage puzzle then eat several Bluecaps']}`
- **추가 정보**: Removes the 75 investment cap on the Intelligence Attribute. The stat requirements to obtain this Talent will be increased to 77 or 78 if your Aspect has increased Intelligence on spawn, though this limitation will be removed if you have the Multifaceted Echo Unlock. The quest requirement for this Talent will be removed if you've obtained it previously on your account.

### Successive Prediction `[Common]`
- **설명**: Predicting an attack will briefly allow you to predict another. | **요구조건**: `{'stats': {'Intelligence': 50}, 'mantras': ['Prediction']}`
- **추가 정보**: Allows you to reflect the entirety of multi-hit moves.

### Twelve Steps Ahead `[Common]`
- **설명**: Landing Prediction will halve the cooldown to a minimum of 2s. Whiffing will double the cooldown to a maximum of 30s. This effect stacks for up to 30 seconds. | **요구조건**: `{'stats': {'Intelligence': 80}, 'mantras': ['Prediction']}`
- **추가 정보**: This effect requires your opponent to be within 90 studs of you. For every point of Intelligence below 80, Prediction's maximum cooldown will be increased by 0.125 seconds, capping at 33.13 seconds with 55 Intelligence.

### Absolute Force `[Faction]`
- **설명**: Evolve the technique of your Oppressive Force, letting both hits of your flourish deal 50% more posture damage. | **요구조건**: `{'talents': ['Oppressive Force'], 'objectives': ['Shock Corps Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: Because the second hit of Oppressive Force cannot receive posture damage modifiers, this Talent only benefits the initial hit of your Oppressive Force flourish.

### Amp Overdrive `[Faction]`
- **설명**: Guardbreaking an opponent causes them to take extra thunder damage and applies Electrify for 7 seconds. | **요구조건**: `{'objectives': ['Shock Corps Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: Deals 15 Thundercall damage. The Electrify status effect changes your opponent's damage type to Thundercall and gives you 10% damage reduction to their attacks.

### Martial Brutality `[Faction]`
- **설명**: The less health your opponent has, the more posture you deal to them. | **요구조건**: `{'objectives': ['Shock Corps Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: Increases your posture damage by 0.1% per 1% health missing, up to a maximum of +10% posture damage against someone at 0% health.

### Shocking Reverb `[Faction]`
- **설명**: Landing enough lightning mantras without getting hit grants you a defensive lightning cloak for 15 seconds, letting you negate damage from light attacks and ironsing. | **요구조건**: `{'objectives': ['Shock Corps Division'], 'origin': 'Authority Ensign'}`
- **추가 정보**: You need to reach a threshold of 150 scaled damage with Thundercall Mantras without being hit to proc this Talent. The damage buildup to reach the threshold is unaffected by resistances and damage modifiers. Also negates damage from critical attacks and Silentheart abilities. 2 minute cooldown.

### Lock n Load `[Common]`
- **설명**: [1H Guns] The first bullet in your gun does more damage when fully loaded. This damage buff scales with the number of bullets up to 15%. | **요구조건**: `{'stats': {'Light Weapon': 60}, 'weaponType': 'Pistol'}`

### Rapid Fire `[Common]`
- **설명**: [1H Guns] When you land a critical shot, gain Rapid Fire for 2s. 12s Cooldown. | **요구조건**: `{'stats': {'Light Weapon': 50}, 'weaponType': 'Pistol'}`
- **추가 정보**: The Rapid Fire status effect entirely removes your Pistol critical cooldown for its duration, allowing you to spam it. Procs on dodge, block, and hit.

### Rapid Reload `[Common]`
- **설명**: [1H Guns] You have 20% faster reload when reloading an empty pistol | **요구조건**: `{'stats': {'Light Weapon': 50}, 'weaponType': 'Pistol'}`
- **추가 정보**: Reduces the total time taken to reload a pistol from empty by 0.1 seconds.

### Sleight of Hands `[Common]`
- **설명**: [1H Guns] When you flourish an opponent you instantly load a bullet. | **요구조건**: `{'stats': {'Light Weapon': 50}, 'weaponType': 'Pistol'}`

### Ultrakill `[Common]`
- **설명**: [1H Guns] When under the effects of Rapid Fire you reload 2X as fast. | **요구조건**: `{'stats': {'Light Weapon': 55}, 'talents': ['Rapid Fire'], 'weaponType': 'Pistol'}`

### Cult of Personality `[Common]`
- **설명**: You gain +3% PEN for each person Charmed, capping at +15% PEN. | **요구조건**: `{'stats': {'Charisma': 90}}`
- **추가 정보**: The PEN gain per target will be reduced if you do not meet Cult of Personality's Charisma requirement.

### Pardon Me `[Common]`
- **설명**: Crimes you commit in allied territories are often ignored. Who's asking? | **요구조건**: `{'stats': {'Charisma': 85}}`
- **추가 정보**: Guards will not aggro onto you if you perform a crime in their territory if you have neutral or higher reputation with the faction.

### Excavator `[Quest]`
- **설명**: Chance to receive two sets of ore when mining, mine ores a lot faster. | **요구조건**: `{'objectives': ['Turn in 5 pure ores at a Blacksmith.']}`

### Harvester `[Quest]`
- **설명**: Chance to receive two sets of ingredients when harvesting. | **요구조건**: `{'objectives': ["Complete Ciea's Quest 3 times."]}`

### Celebrity `[Common]`
- **설명**: Your base reputation with factions is higher and your reputation caps out higher. Reduces the penalty for committing crimes. | **요구조건**: `{'stats': {'Charisma': 40}}`

### Under The Radar `[Common]`
- **설명**: The negative reputation threshold for a faction to put out posters of you is now higher. | **요구조건**: `{'stats': {'Charisma': 60}}`

### You'll Need To Get Past Me `[Common]`
- **설명**: When you're attacked, one of your many allies will leap into action to protect their boss. | **요구조건**: `{'stats': {'Charisma': 75}}`
- **추가 정보**: Spawns in an allied NPC to attack whoever hits you. This Talent can only proc if you are not in combat. The cooldown of this Talent scales on your Charisma investment, having a base cooldown of 69.286 seconds with each investment point into Charisma decreasing this by 0.143 seconds. At requirements, this Talent will have a 59 second cooldown, has a maximum cooldown of 62 seconds at 50 Charisma, and a minimum cooldown of 55 seconds at 100 Charisma.

### Going Nowhere `[Rare]`
- **설명**: When enemies dodge your attacks, their momentum is killed and they're briefly prevented from sprinting. | **요구조건**: `{'stats': {'Strength': 25, 'Agility': 25}}`

### Volcanic Glass `[Advanced]`
- **설명**: Detonating crystals causes an eruption soon after. | **요구조건**: `{'talents': ['Eruption Path: Lava Serpent', 'Glass Path: Crystallization']}`

### Hungry Flames `[Common]`
- **설명**: When you have no Ether, consume Stomach and Water to instantly cast your next fire mantra [15 second CD]. | **요구조건**: `{'stats': {'Flamecharm': 30, 'Fortitude': 15}}`

### Blood Bag `[Common]`
- **설명**: You receive extra blood from knocking an enemy. | **요구조건**: `{'stats': {'Bloodrend': 20}}`

### Blood Transfusion `[Rare]`
- **설명**: Successfully landing a critical attack while under a negative status effect will transfer the effect plus recover a small portion of your blood bar. | **요구조건**: `{'stats': {'Bloodrend': 60}}`
- **추가 정보**: 20 second cooldown.

### Open Wound `[Common]`
- **설명**: Guardbreaking enemies leaves enemies more susceptible to blood loss from Bloodrend mantras. | **요구조건**: `{'stats': {'Bloodrend': 40}}`

### Kj's Courage `[Quest]`
- **설명**: Gain 10% more Knowledge from all sources, rounded down. | **요구조건**: `{'quests': ["Vigil's Savior"]}`
- **추가 정보**: Due to it rounding down, this Talent will only activate if you get at least 10 Knowledge in one instance.

### Nanji's Training `[Quest]`
- **설명**: Nanji shows you a better way to properly block attacks using a weapon, granting you 1 Posture. | **요구조건**: `{'quests': ['Travelling Blade']}`

### Supernatural Sense `[Quest]`
- **설명**: After dealing with literal ghosts, you feel emboldened. | **요구조건**: `{'quests': ['Ghost Hunting']}`

### Bulldozer `[Rare]`
- **설명**: Enemies you flourish into a wall have a chance of breaking the wall and are guard broken on impact. | **요구조건**: `{'stats': {'Strength': 25}}`
- **추가 정보**: This has a 50% chance to break destructible objects when you flourish people into them.

### Broken Ankles `[Common]`
- **설명**: Blockbreaking an opponent puts their Mobility slot Mantras on CD for 12s. | **요구조건**: `{'stats': {'Strength': 70}}`
- **추가 정보**: Broken Ankles' duration will be reduced by 0.15 seconds for every point in Strength below 70, capping at 8.25 seconds with 45 Strength. 30 second cooldown.

### Piercing Blow `[Advanced]`
- **설명**: Attacks that break an opponent's block ignore their Armor resistances. | **요구조건**: `{'stats': {'Strength': 100}}`
- **추가 정보**: Gain +50% PEN on attacks that guardbreak.

### Shield Breaker `[Common]`
- **설명**: Blunt damage now fully ignores the posture bonus from shields. | **요구조건**: `{'stats': {'Strength': 60}, 'talents': ['Unwavering Resolve']}`

### Unwavering Resolve `[Common]`
- **설명**: Getting parried punishes your posture 33% less. | **요구조건**: `{'stats': {'Strength': 40}}`
- **추가 정보**: The posture reduction effect is reduced by 0.433% for every point in Strength below 40, having a minimum value of 22% posture reduction from being parried at 15 Strength.

### Million Ton Piercer `[Advanced]`
- **설명**: Gain 5% extra PEN and remove the cap on your PEN. Go beyond your limits. | **요구조건**: `{'stats': {'Strength': 90}, 'talents': ['Unwavering Resolve', 'Shield Breaker']}`
- **추가 정보**: Removes the 50% cap on Melee PEN.

### Jolting Current `[Common]`
- **설명**: Your lightning attacks in water strike others near them with lightning. | **요구조건**: `{'stats': {'Thundercall': 35}}`
- **추가 정보**: While you and your opponent are in the water, landing any attack that would apply Shock or a Surge Rod will strike other waterborne targets in a 20 stud AoE from the initial target, dealing 50% of the attack's damage and applying Shock or a Surge Rod.

### Rending Needle: Augmenter `[Rare]`
- **설명**: If an enemy has 5 or more rods, your Ironsing Pull will use their rods to form a powerful sword to attack with. This also makes your Metal Armament stronger while the weapon is equipped. | **요구조건**: `{'stats': {'Weapon': 90, 'Ironsing': 90}}`
- **추가 정보**: Replaces your current weapon with the Metal Greatsword for 10 seconds when you Pull an enemy who has 5 Metal Rods on them. While Metal Greatsword is equipped, your Metal Armament damage is increased by 50%.

### Rending Needle: Conductor `[Rare]`
- **설명**: 5 metal rods will combine into a conductor rod. If an enemy uses a non-Ironsing elemental mantra, they're dealt with their element back in return. | **요구조건**: `{'stats': {'Ironsing': 75}, 'talents': ['Master Ironsinger']}`
- **추가 정보**: Upon applying 5 Metal Rods to a target, the Rods will converge into a Conductor Rod. Conductor Rods cannot be pulled. If an enemy affected by a Conductor Rod casts a Mantra, they will lose 5% of their maximum armor, and if that Mantra was a non-Ironsing/Bloodrend elemental Mantra, they will be afflicted with their Attunement's status effect, causing the Rod to fall off. Conductor Rods last 30 seconds or until a non-Ironsing/Bloodrend elemental Mantra is cast.

### Conductor's Cable `[Common]`
- **설명**: Applying Conductor rods on opponents steals some of their armor to you. | **요구조건**: `{'stats': {'Ironsing': 75}, 'talents': ['Rending Needle: Conductor']}`
- **추가 정보**: Creating a Conductor Rod drains 10% of your opponent's maximum armor.

### Rending Needle: Impaler `[Rare]`
- **설명**: If an enemy is affected by 5 or more metal rods, your Ironsing Pull instead pulls out all of the rods for massive damage. | **요구조건**: `{'stats': {'Ironsing': 75}, 'talents': ['Master Ironsinger']}`
- **추가 정보**: Increases the Metal Rod cap from 5 to 10. You can no longer use Metal Pull unless the target has at least 5 rods. Your Metal Pull now deals damage, with the damage scaling based on the amount of Rods applied. Impaler Rods individually have a base damage of 4, with 5 Ironsing scaling, gaining 0.02 damage per Ironsing investment. This will deal 5.5 damage per rod at 75 Ironsing and 6 damage per rod at 100 Ironsing.

### Rending Needle: Jailer `[Rare]`
- **설명**: If an enemy has 5 or more rods, your Ironsing Pull will restrain them for 1s instead of pulling them. | **요구조건**: `{'stats': {'Ironsing': 75}, 'talents': ['Master Ironsinger']}`
- **추가 정보**: Increases the Metal Rod cap from 5 to 10, and you can no longer use Metal Pull unless the target has at least 5 rods. Upon pulling a target, they will be unable to sprint or dodge, for a duration that scales on your Ironsing investment. For every rod you apply past 5, deal 3 damage on your pull, capping at 15 damage at 10 rods.

### Family Recipe `[Quest]`
- **설명**: You can now craft bombs at a crafting bench. | **요구조건**: `{'quests': ['Family Recipe']}`
- **추가 정보**: Bombs are crafted with 2 Iron and 1 Coal. Pressing E while holding a bomb will throw it, while pressing M1 while holding a bomb will drop it at your feet. Bombs have a 5 second cooldown on throw. Bombs do not deal self damage. Bomb damage scales on your Intelligence attribute, dealing 10 damage at 0 Intelligence and scaling up to 45.5 damage at 100 Intelligence. Bombs deal typeless damage, ignoring armor.

### Incendiary Formula `[Common]`
- **설명**: Bombs will set your enemies on fire upon detonation, as well as launch with more force. Bombs will deal 20% increased damage to burning enemies. | **요구조건**: `{'talents': ['Family Recipe']}`
- **추가 정보**: Bombs apply burn on hit. Bombs will deal 20% more damage to burning targets, regardless of where the burn came from.

### Sulphur Surprise `[Common]`
- **설명**: Your cooldown for throwing bombs will be shortened after your first bomb damages an enemy. | **요구조건**: `{'talents': ['Incendiary Formula']}`
- **추가 정보**: Reduces the bomb throw cooldown from 5 seconds to 4 seconds. This only applies to the bomb thrown directly after this Talent procs, not on the bomb that procced this Talent. 20 second cooldown.

### Hot Potato `[Common]`
- **설명**: Gain a large boost of speed after throwing a bomb. Your bombs have a chance to detonate twice. | **요구조건**: `{'talents': ['Family Recipe']}`
- **추가 정보**: This speed boost lasts 2 seconds.

### Explosive Efficiency `[Common]`
- **설명**: Crafting a bomb will yield two bombs. Chance to make three. | **요구조건**: `{'talents': ['Hot Potato']}`

### Pocket Bombs `[Common]`
- **설명**: You have a chance to activate a bomb in your inventory when damaged | **요구조건**: `{'talents': ['Family Recipe']}`
- **추가 정보**: On proc, this consumes 1 Iron Bomb to drop 2 bombs at your feet. This has a 1 second cooldown, with the cooldown activating any time you take damage, even if the effect did not proc.

### Chorus of Souls `[Advanced]`
- **설명**: Alone, the Wisps lack a voice. But surrounded by so many, the frequencies overlap and you hear it true. | **요구조건**: `{'stats': {'Bloodrend': 30, 'Shadowcast': 30, 'Ironsing': 30, 'Galebreathe': 30, 'Thundercall': 30, 'Flamecharm': 30, 'Frostdraw': 30}, 'talents': ['Oath: Oathless']}`
- **추가 정보**: Grants heavily increased health regeneration if you have all Wisps active. If one of your Wisps runs out, or is not equipped this Talent will deactivate until you recast the Wisp. This Talent will not work if you no longer have the Oathless Oath. This healing is reduced by 0.48% for every point in each Attunement stat that is below 30. Having more than 30 points in an Attunement does not compensate for this.

### Will o' Wisp `[Advanced]`
- **설명**: Your mastery over the Wisps of the Song enables you to mediate the innate conflicts between your wisps, allowing any number of Wisps to be active at a time. | **요구조건**: `{'stats': {'Attunement': 25}, 'objectives': ['Attunement Wisp Mantra']}`
- **추가 정보**: Allows the player to have multiple Wisp Mantras active at once.

### Wisp Convergence `[Rare]`
- **설명**: When empowered by the Chorus, your Wisps now grant their elements to your strikes. | **요구조건**: `{'talents': ['Oath: Oathless', 'Chorus of Souls']}`
- **추가 정보**: While Chorus of Souls is active, your weapon attacks will apply Burn, Chill, Shock, Winded, Shadow, Metal Rods, and Blood Poison. This Talent will not activate unless you have every Attunement's Wisp Mantra equipped and active. If one of your Wisps runs out, this Talent will deactivate until you recast the Wisp. This Talent will not work if you no longer have the Oathless Oath.

### Light Weapons Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Light Weapons attribute to its fullest. | **요구조건**: `{'stats': {'Light Weapon': 75}, 'or': [{'quests': ["Vigil's Savior"]}, {'slay': 'Any boss'}]}`
- **추가 정보**: Removes the 75 Attribute cap on Light Weapons.

### Medium Weapons Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Medium Weapons attribute to its fullest. | **요구조건**: `{'stats': {'Medium Weapon': 75}, 'or': [{'quests': ["Vigil's Savior"]}, {'slay': 'Any boss'}]}`
- **추가 정보**: Removes the 75 Attribute cap on Medium Weapons.

### Heavy Weapons Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Heavy Weapons attribute to its fullest. | **요구조건**: `{'stats': {'Heavy Weapon': 75}, 'or': [{'quests': ["Vigil's Savior"]}, {'slay': 'Any boss'}]}`
- **추가 정보**: Removes the 75 Attribute cap on Heavy Weapons.

### Oath: Saintsworn `[Oath]`
- **설명**: A vow to the fallen heroes. Press L to swap to Saintsblade. | **요구조건**: `{'stats': {'Flamecharm': 15, 'Frostdraw': 15, 'Galebreathe': 15, 'Thundercall': 15, 'Shadowcast': 15}, 'objectives': ['Talk to all 5 Obelisks']}`
- **추가 정보**: While the Saintsblade is equipped, your Saintsworn Talents will be activated and you can utilize the Blade of Saints Mantra. By using the Saintsblade's critical attack, you can cycle between the Saint Stances. Each Saint Stance is attributed to one of the Attunements, potentially changing the effects of your Saintsworn Talents and altering your Blade of Saints Mantra.

### Saint's Negation `[Oath]`
- **설명**: Once per stance cycle you can fully block an attack that matches your Saint Stance. | **요구조건**: `{'talents': ['Oath: Saintsworn'], 'or': [{'slay': 'The Doom of Caeranthil'}, {'slay': 'Interluminary Parasol'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Allows you to fully negate the damage of one attack that has a damage type that corresponds with your current Saint Stance. Can only proc once per full cycle, meaning you'll have to fully cycle through all of the Stances before you can proc it again.

### Saint's Overload `[Oath]`
- **설명**: After a full rotation of stances your elemental scaling is increased by 15% and Mantra Modifiers increased by 10%. | **요구조건**: `{'talents': ['Oath: Saintsworn'], 'or': [{'slay': 'The Doom of Caeranthil twice'}, {'slay': 'Interluminary Parasol twice'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Increases your Attunement investment scaling by 15% and the effects of your Mantra modifiers by 10% for a few seconds after performing a full rotation of Saint stances. You'll need to fully cycle through all of the Stances before you can proc this effect again.

### Saint's Synergy `[Oath]`
- **설명**: 15% of your highest element scaling is applied to other elemental damage. | **요구조건**: `{'talents': ['Oath: Saintsworn'], 'or': [{'slay': 'The Doom of Caeranthil twice'}, {'slay': 'Interluminary Parasol twice'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: 15% of the investment scaling from your highest Attuned stat is added to your other Attuned Mantras, granting them slight dual scaling.

### Antithetic Salts `[Oath]`
- **설명**: Alter your brews to invert their effects. Does not count towards the ingredient limit. | **요구조건**: `{'talents': ['Oath: Saltchemist'], 'or': [{'objectives': ['Craft Pluripotent Alloy,Vibrant Gem,Stardust']}, {'objectives': [' Pay 10 Knowledge']}]}`
- **추가 정보**: Gives you a Talent tool-like ability that acts as a potion ingredient on use. When applied to your potions, it inverts the effects of the ingredients in the potion.

### Aromatic Salts `[Oath]`
- **설명**: Alter your brews to create lingering clouds of mist on shattering. Does not count towards the ingredient limit. | **요구조건**: `{'talents': ['Oath: Saltchemist'], 'or': [{'objectives': ['Craft Pluripotent Alloy,Vibrant Gem,Stardust']}, {'objectives': [' Pay 10 Knowledge']}]}`
- **추가 정보**: Gives you a Talent tool-like ability that acts as a potion ingredient on use. This changes your thrown potions to a lingering cloud that lasts for 10 seconds, applying the potion's effects on each hit.

### Biotic Salts `[Oath]`
- **설명**: Alter your brews to not provide their positive effects to your enemies. Does not count towards the ingredient limit. | **요구조건**: `{'talents': ['Oath: Saltchemist'], 'or': [{'objectives': ['Craft Pluripotent Alloy,Vibrant Gem,Stardust']}, {'objectives': [' Pay 10 Knowledge']}]}`
- **추가 정보**: Gives you a Talent tool-like ability that acts as a potion ingredient on use. This halves the negative effects of your potion if used on allies (including yourself) and halves the positive effects of your potions if used on enemies.

### Enhanced Flow `[Common]`
- **설명**: Refine your Rush Hour, allowing you to now also gain temp health whenever you hit a player while using Rush Hour. You now also take less damage from Rush Hour. | **요구조건**: `{'stats': {'Bloodrend': 90, 'Weapon': 90}}`
- **추가 정보**: When you land basic attacks during Rush Hour, gain Temporary Health equal to 30% of your weapon's scaled damage. This cannot give more than 50 Temporary Health in a singular instance. Reduces Rush Hour's self damage by 22%, from 4.5 damage per tick to 3.5 damage per tick. Despite what the description states, this Talent still procs when hitting monsters or other non-player enemies.

### Torture Mastery `[Common]`
- **설명**: Landing a critical on opponents applies 15 seconds of Torture Mastery. Heal any chip damage off players who have Torture Mastery on them. This duration is doubled if you have Rush Hour on. | **요구조건**: `{'stats': {'Bloodrend': 100, 'Weapon': 100}}`
- **추가 정보**: On proc, all chip damage you deal will be converted into healing. The conversion rate is 1:1.

### Dark Receiver `[Common]`
- **설명**: Shadow moves will also steal Ether from those you are Static Linked tethered to. | **요구조건**: `{'stats': {'Thundercall': 40, 'Shadowcast': 40}, 'talents': ['Static Link']}`

### Blood Bank `[Common]`
- **설명**: Consuming 'Charm' now gives slight temporary health. | **요구조건**: `{'stats': {'Bloodrend': 80, 'Charisma': 40}, 'talents': ['Manipulator']}`
- **추가 정보**: Grants 25 Temporary Health on proc. This Talent only procs via Donation Drive and Manipulator. Has an indirect 10 second cooldown due to it relying on Manipulator.

### Sharing is Caring `[Common]`
- **설명**: Charmed on opponents also slightly increases your blood drain against them. | **요구조건**: `{'stats': {'Bloodrend': 50, 'Charisma': 30}, 'talents': ['Charismatic Cast']}`

### Windwaker `[Quest]`
- **설명**: Call upon a gust of wind to propel your boat even faster. | **요구조건**: `{'stats': {'Galebreathe': 20}, 'objectives': ["Complete Stratos' quest"]}`
- **추가 정보**: Grants a Talent tool that can only be used while on a boat and out of combat. On use, the boat will gain a very large amount of additional speed for a short duration.

### Dirty Boxing `[Rare]`
- **설명**: Hitting an enemy with a Basic Attack after feinting applies bleed, obscures their vision slightly and makes PvE enemies Sluggish.  | **요구조건**: `{'stats': {'Agility': 25}, 'weaponType': 'Fists'}`
- **추가 정보**: 8 second cooldown.

### Pocket Sand `[Common]`
- **설명**: [Fist] Feinting into an uppercut blinds, applies Stagger to PvE enemies and also applies Dazed briefly. We're even now, right? 30s cooldown | **요구조건**: `{'stats': {'Light Weapon': 35, 'Strength': 20}}`
- **추가 정보**: 30 second cooldown.

### Gilded Path: Scrapsinger `[Common]`
- **설명**: Flourishing an enemy consumes any rods they have and siphons their armor to you per rod. | **요구조건**: `{'stats': {'Ironsing': 35}}`
- **추가 정보**: Your Ironsing abilities and status effects are now yellow.

### Artisan's Blade `[Common]`
- **설명**: Activating Scrapsinger forges a metal blade behind you for every 2 rods you consume. Metal blades will fire at a target upon landing an ironsing or metal infused attack. | **요구조건**: `{'stats': {'Ironsing': 45}, 'talents': ['Gilded Path: Scrapsinger']}`
- **추가 정보**: Each Artisan Blade has 8 Base damage with 5 Ironsing scaling, gaining 0.04 damage per Ironsing investment. Artisan Rods deal 4.5 posture damage if blocked. Pulling rods normally also procs this Talent. "Metal infused attacks" refers to Ironsing legendary weapon attacks.

### Masterwork `[Rare]`
- **설명**: Successful hits from Artisan's Blades will proc metal rods and deal 50% more damage. | **요구조건**: `{'stats': {'Ironsing': 60}, 'talents': ["Artisan's Blade"]}`

### Refine and Reuse `[Common]`
- **설명**: Consuming rods with Scrapsinger reduces incoming PEN against you for 14 seconds. Each rod reduces PEN by 5% multiplicatively. | **요구조건**: `{'stats': {'Ironsing': 45}, 'talents': ['Gilded Path: Scrapsinger']}`

### Songs Unforged `[Common]`
- **설명**: Your weapon criticals will now activate scrapsinger. | **요구조건**: `{'stats': {'Ironsing': 50}, 'talents': ['Gilded Path: Scrapsinger']}`

### Reshape and Remold `[Advanced]`
- **설명**: Successful procs of Scrapsinger will increase the amount of armor damage your opponent takes. After hitting 10 stacks, the opponent will take +5% damage until the stacks drop below 10. | **요구조건**: `{'stats': {'Ironsing': 70}, 'talents': ['Gilded Path: Scrapsinger', "Artisan's Blade", 'Masterwork', 'Refine and Reuse', 'Songs Unforged']}`
- **추가 정보**: Increases the armor drain effect of your rods by 25%, from 2% drain to 2.5%.

### Gruesome Harvest `[Advanced]`
- **설명**: Landing Bloodrend mantras on opponents with over 70% blood poison will give you slight temporary health. | **요구조건**: `{'stats': {'Bloodrend': 85}}`
- **추가 정보**: Grants 15 flat temporary health on proc. Has a 2 second cooldown.

### Hemolysis `[Common]`
- **설명**: Deal 20% more critical attack damage to opponents with over 25% blood poisoning. | **요구조건**: `{'stats': {'Bloodrend': 40, 'Strength': 25}}`

### Hemolytic Transfusion `[Common]`
- **설명**: Guardbreaking an enemy with a Bloodrend mantra increases the amount of blood poison from the attack. | **요구조건**: `{'stats': {'Bloodrend': 65}}`

### Juicy Snack `[Common]`
- **설명**: Eliminating enemies returns their amount of blood poison as health to you. | **요구조건**: `{'stats': {'Bloodrend': 60, 'Fortitude': 20}}`
- **추가 정보**: The healing gained is 1:1 with Blood Poison applied.

### Panacea `[Rare]`
- **설명**: Hitting an enemy with a Bloodrend mantra stops their blood poison from decaying briefly. | **요구조건**: `{'stats': {'Bloodrend': 65}}`
- **추가 정보**: Lasts 7 seconds.

### Tainted Ground `[Common]`
- **설명**: Enemies who stand in blood pools will not decay blood poison and gain 15% more blood poisoning. | **요구조건**: `{'stats': {'Bloodrend': 30}}`

### Vasculitis `[Common]`
- **설명**: Hitting your opponent while they have over 20% blood poisoning disables their deep gems for a brief duration while giving you Gem Enhancement against PvE temporarily. | **요구조건**: `{'stats': {'Bloodrend': 40, 'Intelligence': 35}}`
- **추가 정보**: On proc, your opponent will be unable to use their Deep Gems for 8 seconds. Gem Enhancement increases the effectiveness of your Deep Gems in PvE.

### Shadowcast Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Shadowcast to its fullest. | **요구조건**: `{'stats': {'Shadowcast': 75}, 'talents': ['Master Shadowcaster'], 'slay': 'Any humanoid boss'}`
- **추가 정보**: Removes the 75 investment cap on the Shadowcast Attribute. This Talent will be removed if you do not meet its stat requirements.

### Shadowcaster `[Common]`
- **설명**: Grants you the ability to command shadows as a Shadowcaster. | **요구조건**: `{'stats': {'Shadowcast': 1}}`

### Adept Shadowcaster `[Common]`
- **설명**: You can now obtain 1-star Leveled Shadowcaster Mantras. | **요구조건**: `{'stats': {'Shadowcast': 20}, 'talents': ['Shadowcaster']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Expert Shadowcaster `[Common]`
- **설명**: You can now obtain 2-star Leveled Shadowcaster Mantras. | **요구조건**: `{'stats': {'Shadowcast': 30}, 'talents': ['Adept Shadowcaster']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Master Shadowcaster `[Common]`
- **설명**: You can now obtain 3-star Leveled Shadowcaster Mantras. | **요구조건**: `{'stats': {'Shadowcast': 50}, 'talents': ['Expert Shadowcaster']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Blossoming Darkness `[Common]`
- **설명**: The more Ether you drain during Shadow Roar, the bigger it gets. | **요구조건**: `{'stats': {'Shadowcast': 40}, 'mantras': ['Shadow Roar']}`

### Fear the Dark `[Common]`
- **설명**: Enemies that run from you after being hit by your shadows will hang in place briefly. | **요구조건**: `{'stats': {'Shadowcast': 50}}`
- **추가 정보**: After you land a Shadowcast Mantra, if your opponent attempts to distance themselves from you, they will be locked in place for 1.5 seconds.

### Lasting Sorrow `[Common]`
- **설명**: Shadows last longer on your opponent. | **요구조건**: `{'stats': {'Shadowcast': 50}}`
- **추가 정보**: Doubles the proc window of Fear the Dark.

### Shadow Travel `[Rare]`
- **설명**: Teleport to a location in exchange for Ether cost. Certain ranges will require a health sacrifice. Be careful as this technique can prove lethal to the user. | **요구조건**: `{'stats': {'Shadowcast': 75}, 'talents': ['Dark God']}`
- **추가 정보**: Deals 0.25 self damage per stud teleported. This can kill you if you don't have enough health to survive the teleport. If your teleport distance is less than 300 studs, you will not take self damage. Drains 100 Ether on use, with each stud travelled increasing this Ether cost by 0.2. The maximum distance you can travel is based on your Ether.

### Sightless Still `[Common]`
- **설명**: The more a person is affected by your Shadowcast the more you obscure their vision. Block breaking an opponent obscures their vision even more and applies Ether Sunder to PvE | **요구조건**: `{'stats': {'Shadowcast': 30}}`

### Singularity `[Common]`
- **설명**: Enemies will briefly hang in place immediately after being hit by a shadow move. | **요구조건**: `{'stats': {'Shadowcast': 40}}`

### Knight's Rally `[Common]`
- **설명**: When using a shield, you ready your block more quickly after taking a hit. | **요구조건**: `{'stats': {'Fortitude': 30, 'Willpower': 10}, 'weaponType': 'Shield'}`

### Turtle Shell `[Common]`
- **설명**: If your shield is on your back, take reduced backstab damage and negate Spine Cutter. | **요구조건**: `{'stats': {'Fortitude': 50}, 'talents': ["Knight's Rally"], 'weaponType': 'Shield'}`
- **추가 정보**: If you have a shield equipped and your main weapon two-handed, your shield will be put on your back. This grants 12.5% damage reduction against attacks that hit your back and prevents your opponent from proccing Spine Cutter.

### Grounding Bolt `[Common]`
- **설명**: Anytime you summon a lightning strike on your oppponent, disable their ability to jump. Uppercutting your opponent while they are unable to jump now strikes them with another bolt of lightning. | **요구조건**: `{'stats': {'Thundercall': 90, 'Weapon': 90}}`
- **추가 정보**: The anti-jump effect lasts 10 seconds and can have its duration refreshed by landing another eligible lightning strike attack. Lightning strikes from Grounding Bolt deal 15 Thundercall damage, and are procced by landing any uppercut, including uppercut-tagged Mantras. The lightning strikes have no cooldown, and can be caused by uppercutting a target who is under the effect of any anti-jump status effect, such as Taunt or Bear Trap; it does not explicitly have to be Grounding Bolt's anti-jump for the lightning strikes to trigger. Apply the Grounding Bolt effect by landing lightning strikes from Scorched Peak, Fulgurite Formation, the Specialist Set equipment Talents, and Storm/Stormbreaker enchantments during the rain.

### Silencer's Blade `[Rare]`
- **설명**: Meleeing a 'Suffocated' opponent will extend the duration of the Suffocation and grant a speed boost. | **요구조건**: `{'stats': {'Power': 10, 'Galebreathe': 60}}`
- **추가 정보**: Landing M1 attacks or criticals with the M1 tag on suffocated targets applies a new stack of suffocation that lasts 5 seconds. Grants a 22.5% speed boost for 3 seconds on proc.

### A World Without Song `[Advanced]`
- **설명**: Every 3 hits with a Wind Mantra now procs Suffocating. | **요구조건**: `{'stats': {'Galebreathe': 75}, 'talents': ["Silencer's Blade"]}`
- **추가 정보**: Scales down to 4 hits when under 75 Galebreathe, and 5 hits when under 40 Galebreathe.

### Oath: Silentheart `[Oath]`
- **설명**: You vow to reject the Words of the Song, denying yourself of mantras in pursuit of your own path to true strength, no matter the cost. You can wield weapons with 25 points below their usual requirements. | **요구조건**: `{'stats': {'Strength': 25}, 'add': [{'stats': ['Light Weapon', 'Medium Weapon', 'Heavy Weapon'], 'value': 75}], 'or': [{'stats': {'Agility': 25}}, {'stats': {'Charisma': 25}}]}`
- **추가 정보**: If you have any Mantras, they will be unusable and will be entirely invisible. The weapon requirement reduction effect only reduces weapon stat requirements, and not attribute requirements. Additionally, it stacks with Khan's Versatile. Silentheart abilities can proc the Enchantment of your equipped weapon with a 30 second cooldown.

### Dread Fighter `[Oath]`
- **설명**: Parrying and getting hit by mantras now give you stacks of Dread. Each stack lasts for 15 seconds. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': 'X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: Each stack of Dread Fighter grants 5% Mantra damage reduction, capping at 5 stacks for 25% Mantra damage reduction.

### Flow State `[Oath]`
- **설명**: Enter a moment of extreme focus in which you can change the windup of your special attacks with the correct timing. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': '"X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: Activating Ankle Cutter, Mayhem, Relentless Hunt, or Rising Star within 2 seconds of activating Flow State will enhance these attacks. Flow State has a 10 second cooldown, but landing a Flow State-enhanced Silentheart ability will reset its cooldown. Flow State may affect the damage, wind-up, number of attacks, sound effect, or properties of Silentheart abilities.

### Mayhem `[Oath]`
- **설명**: Initiate a special dash attack by pressing M1 during the start of your dodge. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': '"X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: 16s CD per weapon type, 6s CD if feinted. Movesets and damage differ depending on weapon type. Gains the ability to autogrip if it is enhanced by Flow State.

### Relentless Hunt `[Oath]`
- **설명**: M1 while doing an Aerial Attack to initiate a special gap closer attack. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': '"X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: 20s CD per weapon type, 6s CD if feinted. Movesets differ depending on weapon type. The Light Weapon variant hits twice if it is enhanced by Flow State.

### Rising Star `[Oath]`
- **설명**: Press CTRL + M2 to activate a special uppercut attack. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': '"X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: 12s CD per weapon type, 4s CD if feinted. Procs all "on Uppercut" Talents. Movesets differ depending on weapon type.

### Silent Cascade `[Oath]`
- **설명**: Landing physical attacks on an opponent charges up your Silent Cascade, a devastating barrage that can be released with CTRL + M2. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': '"X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: Landing 8 weapon attacks or Silentheart abilities grants the Silent Cascade status effect, allowing you to use the Silent Cascade attack. This effect lasts 30 seconds or until you use Silent Cascade. Deals 7.5 Oath damage per hit (6).

### True Vantage `[Oath]`
- **설명**: Venting makes you invisible briefly, as well as boosting your speed. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': 'X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: Changes your Vent color to match the color of your Silentheart Tattoos.

### Unmatched Dexterity `[Oath]`
- **설명**: Press X to Quick Swap between weapons within your toolbar. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': '"X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: You can now swap weapons and equipment while in combat. Pressing X will swap your current weapon with a random weapon in your hotbar. The keybind can be changed in settings.

### Vengeful Pursuit `[Oath]`
- **설명**: Your running attacks that don't hit send out a special mid-range crescent projectile that slows on hit. Tracks onto those with their backs turned to you. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': '"X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: Base damage and scaling differ depending on weapon type. 8 second cooldown.

### Golden Tongue `[Rare]`
- **설명**: Typing or using a gesture gives a random buff to you and those around you. (60 second cooldown) | **요구조건**: `{'stats': {'Charisma': 40}}`
- **추가 정보**: This can either restore 30% of your maximum Ether or grant 10% damage reduction with a visual effect similar to Reinforce. The buff given to each player is rolled independently. Golden Tongue has a 70 second cooldown at 0 Charisma, with every Charisma invest reducing its cooldown by 0.25 seconds.

### Snake Oil `[Common]`
- **설명**: Gain 40% more Notes from selling items. This is getting downright criminal. But I'm just a talent description, I can't stop you. | **요구조건**: `{'stats': {'Charisma': 30}}`

### Absolute Pitch `[Advanced]`
- **설명**: You can cast Ritual Mantras instantly. | **요구조건**: `{'stats': {'Intelligence': 100}}`
- **추가 정보**: If you have less than 100 Intelligence, this will instead halve the required Ritual Keys (rounded up).

### Ether Overdrive `[Advanced]`
- **설명**: Gain 5% extra PEN and remove the cap on your PEN. Go beyond your limits. | **요구조건**: `{'stats': {'Intelligence': 90}}`
- **추가 정보**: Removes the 50% cap on Mantra PEN.

### Bloodiron Spirit `[Rare]`
- **설명**: You regain some Armor upon killing enemies.
- **추가 정보**: Restores 2.5% of your maximum armor upon executing an enemy.

### Oath: Soulbreaker `[Oath]`
- **설명**: The sum of your fragments is greater than the whole. Though your very being is splintered and threatening to drift apart, every shard of you Vows to remain One. Your Oath is a solvent that joins all of your distinct selves into the gestalt you. | **요구조건**: `{'add': [{'stats': ['Willpower', 'Charisma'], 'value': 50}], 'or': [{'objectives': ['Have Hero reputation with Etris, Have a bell, Talk to Theadre and Yunshul']}, {'objectives': ["Use a Sinner's Ash inside Duke's manor after clearing it"]}]}`
- **추가 정보**: Your Ardour gains a new visual effect.

### Soul Infusion `[Oath]`
- **설명**: Infuse Ardour into your executions. If your execute is interrupted, the opponent remains down for a longer amount of time. Your Ardour Screams are projected further. | **요구조건**: `{'talents': ['Oath: Soulbreaker'], 'objectives': ["Talk to X amount of Shrine's"]}`
- **추가 정보**: Increases your execution speed by 40%, down to 1.8 seconds from 3 seconds. Upon successfully performing an execution, use Ardour Scream for free. Your Ardour Scream range is buffed, sfx is changed, and minimum Ether cost required to cast Ardour Scream is reduced from 100% Ether to 40%.

### Formless `[Oath]`
- **설명**: Teleport to a location within your Tacet bubble. Receive a slight speed boost when activating Tacet. | **요구조건**: `{'talents': ['Oath: Soulbreaker'], 'objectives': ["Talk to X amount of Shrine's"]}`
- **추가 정보**: Grants a Talent tool that costs 50 Ether with a 5 second cooldown. This tool allows you to teleport to your cursor's location, but you cannot teleport outside of the Tacet bubble. On teleport, Tacet will end early. The speed boost gained from using Tacet lasts 2.5 seconds.

### Heart Reverb `[Oath]`
- **설명**: Those picked up by your Rhythm are marked for 8 seconds. Whenever an opponent dodges your attack, detect their rhythm and vigor. You can use Rhythm while standing. | **요구조건**: `{'talents': ['Oath: Soulbreaker'], 'objectives': ["Talk to X amount of Shrine's"]}`
- **추가 정보**: If someone performs an action within Rhythm's range, they will be highlighted red, even through walls. Rhythm will now stay active after uncrouching, only deactivating if done so manually or if you take damage. If an enemy dodges your attack, their health and posture percentages will be displayed in text next to their character briefly.

### Haunted Path: Specter `[Common]`
- **설명**: Build up spectral energy by performing successful dodges and landing Wind mantras. Your abilities no longer suffocate enemies. | **요구조건**: `{'stats': {'Galebreathe': 50}, 'talents': ['Haunted Gale']}`
- **추가 정보**: Turns your Galebreathe white. Increases the potency of your Winded from a 5% swing decrease to 15%.

### Phantom Step `[Common]`
- **설명**: Press X to begine running at high speeds. While in Phantom Step, your dashes transform into Gale Dashes. (Must have at least 10% Spectral Gauge) | **요구조건**: `{'stats': {'Galebreathe': 55}, 'talents': ['Haunted Path: Specter']}`
- **추가 정보**: Additionally grants a speed boost for the full duration. While active, your Spectral Gauge will be passively drained.

### Vanishing Wraith `[Rare]`
- **설명**: Your 'Aerial Attacks' while in Phantom Step will now teleport you behind your target. | **요구조건**: `{'stats': {'Galebreathe': 60}, 'talents': ['Phantom Step']}`

### Possession `[Advanced]`
- **설명**: After an apparition hits an enemy, receive 7.5% posture damage on all Galebreath attacks for 8 seconds. If the apparition hits while you have Phantom Step active, receive a 7.55% chip damage buff for 6 seconds. | **요구조건**: `{'stats': {'Galebreathe': 75}, 'talents': ['Haunted Path: Specter']}`
- **추가 정보**: The chip damage buff only applies to Galebreathe Mantras.

### Oath: Starkindred `[Oath]`
- **설명**: You vow to feel the knowledge of all that is, all at once. Your heart beats with the world itself, as the Stars above watch over you. | **요구조건**: `{'stats': {'Strength': 40}, 'objectives': ['Talk to Samael in the Derelict Highchurch (Songseeker Wilds) and kill Iblis, The Fallen Angel, then return to Samael.']}`

### Death From Above `[Oath]`
- **설명**: Upon cancelling your Air Dash, reveal your wings and strike your enemy. | **요구조건**: `{'talents': ['Oath: Starkindred'], 'or': [{'slay': 'Sinners Abaddon, Minos, and Astaroth'}, {'objectives': ['Pay 10 Knowledge to Samael']}]}`
- **추가 정보**: Air dash canceling with your weapon equipped grants your Starnkindred Wings. Air dash canceling with your weapon equipped and your wings out performs a three hit slashing attack that deals 25 Oath/Slash damage per hit. Deals 15 Posture damage per hit.

### Ichor Imbuement `[Oath]`
- **설명**: Using a Starkindred mantra while your wings are not out increases the damage they deal by 2 times. | **요구조건**: `{'talents': ['Oath: Starkindred'], 'or': [{'slay': 'Sinners Abaddon, Minos, and Astaroth'}, {'objectives': ['Pay 10 Knowledge to Samael']}]}`
- **추가 정보**: Buffs any Starkindred Mantra if your wings are not out on cast.

### Static Link `[Common]`
- **설명**: Flourishing or uppercutting an enemy creates a static link between you and your enemy. | **요구조건**: `{'stats': {'Thundercall': 40, 'Intelligence': 15}}`
- **추가 정보**: Lasts 15 seconds. The links are non-refreshable, meaning you will need to wait until after the duration ends to reapply them.

### Jumper Cables `[Common]`
- **설명**: Being made Unconscious with an active tether allows you to steal health from a tethered target and not be made Unconscious. | **요구조건**: `{'stats': {'Thundercall': 40, 'Fortitude': 20}, 'talents': ['Static Link']}`
- **추가 정보**: Whenever you would get knocked but have a tether active, steal HP from the target to survive the hit. This has a 4 second cooldown.

### Link Conduction `[Common]`
- **설명**: While you have active tethers your lightning mantras cost less ether. | **요구조건**: `{'stats': {'Thundercall': 65}, 'talents': ['Static Link']}`
- **추가 정보**: Each active Link reduces the Ether cost of your Thundercall Mantras by 30%.

### Static Ace `[Common]`
- **설명**: Using Lightning Stream with an active tether link targets your closest active link. | **요구조건**: `{'stats': {'Thundercall': 70}, 'talents': ['Static Link']}`
- **추가 정보**: Heavily reduces the windup of Lightning Stream.

### Static Allure `[Common]`
- **설명**: Having two active tethers will cause the previous tethered enemy to get magnetized to your newest tethered enemy, also increases the duration of tethers by 15 seconds. | **요구조건**: `{'stats': {'Thundercall': 50, 'Intelligence': 15}, 'talents': ['Static Link']}`
- **추가 정보**: Instantly procs when you create a new Static Link. The extra Link duration only applies to the Static Link that procced the magnetization effect.

### Storm Link `[Common]`
- **설명**: While you have a Static Link on someone, your Wind mantras that hit them are imbued with flashes of Lightning. | **요구조건**: `{'stats': {'Thundercall': 60, 'Galebreathe': 50}, 'talents': ['Static Link']}`
- **추가 정보**: Adds a secondary instance of damage to your Galebreathe Mantras if they hit a Static Linked target. This deals 10% of your attack's scaled damage as Thundercall damage.

### Grasp on Reality `[Common]`
- **설명**: Damage taken from insanity is reduced. | **요구조건**: `{'stats': {'Fortitude': 25, 'Willpower': 5}}`
- **추가 정보**: Reduces damage taken from Scratching.

### Magical Resolve `[Common]`
- **설명**: Being hit increases Ether regen for a short duration, the strength of the regen scales off your Willpower. | **요구조건**: `{'stats': {'Willpower': 40}, 'talents': ['Battle Tendency']}`

### Unfazed `[Common]`
- **설명**: You are more resilient to the side effects of going insane. You no longer Shiver and you Panic with less severity. | **요구조건**: `{'stats': {'Willpower': 50, 'Fortitude': 50}, 'talents': ['Grasp on Reality']}`
- **추가 정보**: You now shiver at tier 2 Insanity instead of Tier 1. You now scratch yourself at tier 3 Insanity instead of tier 2. You can no longer Panic.

### Voltaic Conductor `[Common]`
- **설명**: Your Thundercall Mantras deal 30% chip damage against enemies with conductor rods. | **요구조건**: `{'stats': {'Thundercall': 40, 'Ironsing': 75}, 'talents': ['Rending Needle: Conductor']}`

### Iron Gut `[Common]`
- **설명**: You have resistance against being poisoned by foods. | **요구조건**: `{'objectives': ['Vomit once'], 'or': [{'stats': {'Fortitude': 20}}, {'stats': {'Willpower': 20}}]}`
- **추가 정보**: Heavily reduces the chance that you vomit upon eating bad food. This does not work on Pufferfish.

### Termite `[Common]`
- **설명**: You can eat things most would consider inedible. | **요구조건**: `{'stats': {'Fortitude': 20, 'Willpower': 10}}`
- **추가 정보**: Allows user to eat Sticks, Bamboo, Beeswax, Coral, Spider Eggs, all Lotuses, and every Ore.

### Dustlunge `[Advanced]`
- **설명**: You can now assassinate your enemies from much farther, shadestepping to their location if they're too far. Assassinating an enemy will automatically assassinate other nearby enemies. | **요구조건**: `{'stats': {'Agility': 90}, 'talents': ['Lowstride', 'Unseen Threat', 'Deep Wound', 'Lights Out']}`

### None Left Behind `[Common]`
- **설명**: You can now shadestep to pick up Unconscious humanoids far away from you. | **요구조건**: `{'stats': {'Agility': 100}, 'talents': ['Dustlunge']}`

### Foolish Outburst `[Common]`
- **설명**: Blocking or parrying a vent will absorb the Tempo cost of the vent. A Tactician steadies the course of battle. | **요구조건**: `{'stats': {'Intelligence': 50}}`
- **추가 정보**: Steals 40% of the Tempo used. Every point in Intelligence below 50 will reduce the Tempo steal by 0.66%, capping at a minimum of 23.33% of the Tempo absorbed with 25 Intelligence.

### Hard Read `[Common]`
- **설명**: Hitting your opponent during a feint will cause them to be Dazed. | **요구조건**: `{'stats': {'Intelligence': 20}}`
- **추가 정보**: Applies Daze for 1 second.

### Punishing Blow `[Rare]`
- **설명**: [Heavy Weapons] Daze opponents for 1s and Stagger PvE enemies for 2s when you interrupt their Basic Attack / actions with your own. | **요구조건**: `{'stats': {'Heavy Weapon': 20}}`
- **추가 정보**: If you M1 your opponent during their M1 animation, they will be dazed for 1 second. Also procs if you land a critical with the M1 tag during their M1 animation.

### Target Switch `[Common]`
- **설명**: Parrying an opponent then hitting someone else makes your next mantra free. | **요구조건**: `{'stats': {'Intelligence': 20}}`
- **추가 정보**: This effect is signalled by a yellow halo. Has a 4 second activation window with a 10 second duration.

### Water off a Duck's Back `[Common]`
- **설명**: Venting will shift any elemental status effects affecting you onto those hit by your vent. | **요구조건**: `{'stats': {'Intelligence': 50}}`
- **추가 정보**: Transfers Suffocation, Winded, Chill, Shock, Burn, and potion effects from yourself to your enemy on vent.

### Controlled Combustion `[Common]`
- **설명**: Your Agitating Spark no longer spreads to your allies. | **요구조건**: `{'stats': {'Charisma': 40}, 'talents': ['Agitating Spark']}`
- **추가 정보**: Your Agitating Spark cannot spread to you either.

### Artisan Chef `[Common]`
- **설명**: The food you cook now becomes Artisan food, increasing its hunger and thirst gained by +25%. | **요구조건**: `{'stats': {'Intelligence': 25, 'Charisma': 15}, 'objectives': ['Cook 50 Food items (batch cooking does not count).']}`
- **추가 정보**: Increases food nutritional value by 25%. Increases the healing gained from using Fondant Splitter's critical.

### Master Chef `[Common]`
- **설명**: Buffs applied by food you cook now have their buff effects amplified by +30%. | **요구조건**: `{'stats': {'Intelligence': 25, 'Charisma': 15}, 'objectives': ['Cook 50 Food items (batch cooking does not count).']}`
- **추가 정보**: Increases the duration of food buffs by 30%. Increases the healing gained from using Fondant Splitter's critical.

### Explosive Finish `[Common]`
- **설명**: If an enemy is on fire when you flourish, blast them away with a fire blast. | **요구조건**: `{'stats': {'Flamecharm': 45}}`
- **추가 정보**: Deals 5 Flamecharm damage. Upon proccing Emperor Flame, this Talent will be put on a 3s cd.

### Flaming Flourish `[Common]`
- **설명**: Set enemies on fire when you flourish or uppercut them. | **요구조건**: `{'stats': {'Flamecharm': 30}}`

### Emperor Flame `[Common]`
- **설명**: Absorb fire produced by you, once you reach 5 stacks your next attack will be an automatic Explosive Finish flourish. This flourish will deal additional damage and proc Wither, reducing your opponent's maximum health temporarily. | **요구조건**: `{'stats': {'Flamecharm': 60}, 'talents': ['Agitating Spark']}`
- **추가 정보**: Agitating Spark procs grant Emperor Flame stacks. At 5 stacks, gain the Emperor Flame status effect for 10 seconds, causing your next M1 to instantly proc Explosive Finish, dealing 15 Flamecharm damage. On top of this, this will deal an additional 25 Wither damage and apply burn. Emperor Flame also extinguishes self-applied burn through Agitating Spark. While Emperor Flame is on cooldown, the burn will not be extinguished and you cannot gain additional stacks. 30 second cooldown.

### Mirage Clone `[Rare]`
- **설명**: Successfully dodging leaves behind a heat mirage clone that sets enemies that swung at you on fire. | **요구조건**: `{'stats': {'Flamecharm': 65}}`
- **추가 정보**: 20 second cooldown. Causes an Eruption instead if you have Eruption path.

### Grasp of Eylis `[Origin]`
- **설명**: You can temporarily teleport to locations near your bounty target, if one can be found. However, you must stay close, or be desynchronized. | **요구조건**: `{'origin': 'Voidwalker'}`
- **추가 정보**: Grants a Talent tool that can only be used in the Voidheart, teleporting you to your Bounty target. Choosing Stealth causes teleports you near, but far away from your target, hiding the bounty target. Choosing Ferocity teleports you close to your target, highlighting them through walls briefly. If Ferocity is chosen, your character will be enveloped in shadows, signifying that you have a bounty.

### Voideye `[Origin]`
- **설명**: Voidmother's blessing, the method to travel back to the Voidheart. | **요구조건**: `{'origin': 'Voidwalker'}`
- **추가 정보**: Grants a Talent tool that teleports you back to the Voidheart on use. 1 minute cooldown.

### Voidwalker Contract `[Origin]`
- **설명**: You progress much faster from completing bounties, and less from events. Gain access to the Voidheart, and factions have a negative outlook on you. | **요구조건**: `{'origin': 'Voidwalker'}`
- **추가 정보**: Gain increased EXP from bounties of all kinds, but gain reduced EXP from all other sources.

### Cap Artist `[Common]`
- **설명**: Pressing CapArtist while crouching allows you to fake being dead. You also take a bit less damage from PvE while ragdolled as well. | **요구조건**: `{'stats': {'Agility': 25, 'Charisma': 5}}`
- **추가 정보**: This can be deactivated by using the keybind again. Innately bound to Comma.

### Pickpocket `[Common]`
- **설명**: Gain the ability to pickpocket by pressing N. Deal a little more damage the more notes you have against PvE opponents as well. | **요구조건**: `{'stats': {'Agility': 5, 'Charisma': 10}}`
- **추가 정보**: You can only pickpocket Unconscious targets. Gain +0.0002% PvE damage for every 1 Note you have; grants +3% damage at 15,000 Notes.

### Discharge `[Common]`
- **설명**: [Light Weapons] On 5th successful attack you will discharge static dealing lightning damage to those nearby. | **요구조건**: `{'stats': {'Light Weapon': 20, 'Thundercall': 15}}`
- **추가 정보**: Deals 5 Thundercall damage with 5 Thundercall scaling, gaining 0.025 damage per point in Thundercall. Applies Shock or 1 Surge Rod on proc.

### Rain of Static `[Common]`
- **설명**: After successfully casting lightning impact, strike down countless thunder at those below. In return your Lightning Impact will require more time to cast. | **요구조건**: `{'stats': {'Thundercall': 1}, 'mantras': ['Lightning Impact']}`
- **추가 정보**: When casting Lightning Impact, hover above the ground and fire multiple projectiles. Afterward, you strike down normally.

### Windup Battery `[Common]`
- **설명**: Landing 3 Thundercall Mantras without whiffing reduces the windup of your next Mantra by 10%. | **요구조건**: `{'stats': {'Thundercall': 30, 'Intelligence': 30}}`
- **추가 정보**: Applies this bonus to non-Thundercall Mantras.

### Static Blade `[Common]`
- **설명**: Hitting blocks, blocking or parrying hits will now generate an electric charge in your blade, granting a small speed buff. Charges can stack up to 5 times. | **요구조건**: `{'stats': {'Medium Weapon': 20, 'Thundercall': 40}, 'weaponType': 'Medium Weapon'}`
- **추가 정보**: Grants stacks when you '''get parried''', not when you parry attacks. Also grants stacks when you hit blocks or block attacks. Each stack lasts for 15 seconds and refresh upon gaining another, including when you're at max stacks. Each stack grants an ~2.35% speed boost, totaling to ~11.75% speed at max stacks.

### Gathering Electricity `[Common]`
- **설명**: Reaching 5 Static Blade charges will now consume the stacks and apply a lightning buff to your blade. 60 second cooldown. | **요구조건**: `{'stats': {'Thundercall': 65}, 'talents': ['Static Blade'], 'weaponType': 'Medium Weapon', 'or': [{'stats': {'Strength': 25}}, {'stats': {'Agility': 25}}]}`
- **추가 정보**: Clears all Static Blade stacks on proc. You can still gain Static Blade stacks while Gathering Electricity is active. For 15 seconds, this increases the base damage on your weapon attacks, including criticals by 3.

### Overcharge `[Common]`
- **설명**: Your next dash after activating Static Blade is enhanced by lightning. | **요구조건**: `{'talents': ['Gathering Electricity']}`
- **추가 정보**: Lightning Dashes increase your dash distance travelled by 2.3x and the duration of i-frames from rolling, but will end early if you attack.

### Thundercall Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Thundercall to its fullest. | **요구조건**: `{'stats': {'Thundercall': 75}, 'talents': ['Master Thundercaller'], 'slay': 'Any humanoid boss'}`
- **추가 정보**: Removes the 75 investment cap on the Thundercall Attribute. This Talent will be removed if you do not meet its stat requirements.

### Thundercaller `[Common]`
- **설명**: Grants you the ability to command Lightning as a Thundercaller. | **요구조건**: `{'stats': {'Thundercall': 1}}`

### Adept Thundercaller `[Common]`
- **설명**: You can now obtain 1-star Thundercaller mantras. | **요구조건**: `{'stats': {'Thundercall': 20}, 'talents': ['Thundercaller']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Expert Thundercaller `[Common]`
- **설명**: You can now obtain 2-star Thundercaller mantras. | **요구조건**: `{'stats': {'Thundercall': 30}, 'talents': ['Adept Thundercaller']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Master Thundercaller `[Common]`
- **설명**: You can now obtain 3-star Thundercaller mantras. | **요구조건**: `{'stats': {'Thundercall': 50}, 'talents': ['Expert Thundercaller']}`
- **추가 정보**: This Talent will be removed if you do not meet its stat requirements.

### Discovery of Fire `[Common]`
- **설명**: Flints and Flamecharm are for simpletons. | **요구조건**: `{'stats': {'Thundercall': 50}}`
- **추가 정보**: Grants the Discovery of Fire Talent tool that consumes 20 Ether to cause a lightning strike after a 1 second delay. On hit, this deals 3 Thundercall damage and lights all nearby entities and campfires on fire.

### Shocking Finish `[Common]`
- **설명**: Following a flourish up with a lightning beam causes it to be casted instantly. | **요구조건**: `{'stats': {'Thundercall': 30}, 'mantras': ['Lightning Beam']}`

### Static Fakeout `[Rare]`
- **설명**: Roll cancelling immediately after a parry will cause you to teleport behind your opponent. | **요구조건**: `{'stats': {'Agility': 30, 'Thundercall': 35}}`

### Static Flash Clone `[Common]`
- **설명**: When using lightning clones you instead disappear leaving behind a static clone for a short duration. | **요구조건**: `{'stats': {'Agility': 30, 'Thundercall': 35}, 'mantras': ['Lightning Clones']}`

### Manipulator `[Common]`
- **설명**: Deal 20% more critical attack damage to charmed enemies, but the effect is removed on impact. | **요구조건**: `{'stats': {'Charisma': 60}, 'talents': ['Charismatic Cast']}`
- **추가 정보**: 10 second cooldown. This is inherently weaker on multihit criticals due to it only proccing once then going on cooldown. Unnecessary Theatrics or Overcharm can be used to reapply the Charm after Manipulator removes it on the same hit.

### Narcissist `[Common]`
- **설명**: Charming an already Charmed opponent Overcharms you briefly. Guess you really were always that great. | **요구조건**: `{'stats': {'Charisma': 60}, 'talents': ['Charismatic Cast']}`
- **추가 정보**: Overcharms yourself for 4 seconds. Charms yourself for 8 seconds, halved to 4 seconds if you have Disbelief.

### Sow and Mend `[Rare]`
- **설명**: Sacrifice 35% of your blood for temporary health. | **요구조건**: `{'stats': {'Bloodrend': 60}, 'talents': ['Master Bloodrender']}`
- **추가 정보**: Gives 25 flat Temporary Health on use. 30 second cooldown.

### Cyclical Exsanguination `[Common]`
- **설명**: Whenever you deal more than 20 damage to an enemy in an instance, pause your temporary health decay for 3 seconds. | **요구조건**: `{'stats': {'Bloodrend': 65}, 'talents': ['Sow and Mend']}`
- **추가 정보**: 8 second cooldown.

### Embolism `[Common]`
- **설명**: If an enemy is guardbroken while you have temporary health, convert your temporary health into additional damage. | **요구조건**: `{'stats': {'Bloodrend': 65}, 'talents': ['Sow and Mend']}`

### Hypovolemic Focus `[Common]`
- **설명**: While you have temporary health, your opponent regains far less posture from parrying you. | **요구조건**: `{'stats': {'Bloodrend': 65}, 'talents': ['Sow and Mend']}`
- **추가 정보**: The opponent regains 20% less posture damage from parrying you.

### Cheap Shot `[Rare]`
- **설명**: Your attacks gain 10% PEN multiplicatively when you have an active speed boost. | **요구조건**: `{'stats': {'Agility': 65}}`
- **추가 정보**: Multiplies your PEN by 1.1x at 65+ Agility. Cheap Shot's PEN multiplier will be reduced by 0.11% for every point in Agility below 65, having a minimum multiplier of +7.22% PEN (or 1.072x PEN) at 40 Agility.

### Crippling Comeuppance `[Advanced]`
- **설명**: Landing Revenge puts your opponent's Mobility slot Mantras on CD and applies Sluggish to PvE enemies for 15s. | **요구조건**: `{'stats': {'Agility': 100}, 'mantras': ['Revenge']}`
- **추가 정보**: 30 second cooldown. For every point of Agility below 100, Crippling Comeuppance's duration is reduced by 0.1 seconds, having a minimum duration of 12.5 seconds at 75 Agility.

### Down Comes the Claw `[Common]`
- **설명**: Landing a Critical while you have a speed boost prevents your opponent from being able to dodge twice in a row for 5s. | **요구조건**: `{'stats': {'Agility': 75}}`
- **추가 정보**: Lasts 6.5 seconds despite what the description states. You cannot reapply this effect if it is currently active. For every point in Agility under 75, Down Comes the Claw loses 0.055 seconds of duration, capping at a minimum of 5.11 seconds with 50 Agility.

### Maiming Claws `[Common]`
- **설명**: Down Comes the Claw now disables your opponent's posture regeneration for 6s on proc. | **요구조건**: `{'stats': {'Agility': 100}, 'talents': ['Down Comes the Claw']}`
- **추가 정보**: While their posture is paused, your opponent cannot restore posture by parrying, spitting, passive posture restoration, or through Steady Nerves. All other forms of posture restoration ignore this effect entirely. Maiming Claws' duration will be shortened if you do not meet its requirements. Maiming Claws cannot be refreshed if Down Comes the Claw is currently active.

### Pursuit `[Common]`
- **설명**: If you land your Revenge, clear the cooldown immediately. (25s cooldown) | **요구조건**: `{'stats': {'Agility': 90}, 'mantras': ['Revenge']}`
- **추가 정보**: Procs even if Revenge is blocked, parried, dodged, or vented. For every point in Agility below 90, Pursuit will gain +0.375 seconds to its cooldown, capping at 29.4 seconds with 65 Agility.

### Face Cutter `[Rare]`
- **설명**: Your Spine Cutter now deals an additional hit. | **요구조건**: `{'stats': {'Medium Weapon': 75}, 'talents': ['Spine Cutter'], 'weaponType': 'Twinblade'}`
- **추가 정보**: Grants an additional hit to your Spine Cutter that deals 25% of your weapon's scaled damage. Similarly to Spine Cutter, the damage of this attack cannot be buffed and it has no PEN.

### Turning of the Wheel `[Rare]`
- **설명**: After perfect dodging a swing or critical attack, step backwards and ramp up your swingspeed. | **요구조건**: `{'stats': {'Medium Weapon': 75}, 'weaponType': 'Twinblade'}`
- **추가 정보**: Using an M1 after dodging a weapon attack will cause you to step back and then advance with faster swing speed.

### Wraith Path: Twisted Puppets `[Common]`
- **설명**: Your Flamecharm mantras summon puppets of shadow and flame. Your flames are now black. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Shadowcast': 40}}`
- **추가 정보**: Your Flamecharm abilities and status effects are now black. Your regular burn is now much weaker, dealing 87.5% less damage, but it now spawns Puppets on a 4 second cooldown. Your Shadowcast abilities can now apply burn that deals 75% less damage than default burn. Both of these burn types drain 6.25 Ether from affected targets per tick. Puppets deal 20 Typeless damage and 10 posture damage. Increases the uptime of your Flame of Denial by 25%.

### Burning Puppets `[Common]`
- **설명**: Your puppets can now inflict burn and fire-based Talents when they explode. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Shadowcast': 40}, 'talents': ['Wraith Path: Twisted Puppets']}`
- **추가 정보**: Grants your Puppets 5 Flameharm scaling, increasing their damage by 0.1 per Flamecharm investment. Your Puppets now apply 'Puppet Burn', allowing you to create more Puppets. Despite what the Talent description states, your Puppets don't proc any Flamecharm Talents.

### Burning Sacrifice `[Rare]`
- **설명**: Sacrifice puppets who have been alive for half of their lifetime and burn purple for Emperor Flame Stacks, a damage boost per puppet, and a slight speed boost. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Shadowcast': 40}, 'talents': ['Wraith Path: Twisted Puppets', 'Emperor Flame']}`
- **추가 정보**: Puppets will turn purple if they've gone 15 seconds without hitting anything. You can sacrifice these purple Puppets with this Talent tool, granting a 4% damage buff per Puppet sacrificed (caps at 12%) and a small speed boost for 6 seconds. Additionally this grants 1 Emperor Flame stack per Puppet sacrificed. This has a 15 second cooldown if a Puppet is successfully sacrificed, and a 1 second cooldown if not.

### Explosive Rage `[Common]`
- **설명**: Causing explosion will make your puppets go into a frenzy, speeding up and dealing 50% more damage. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Shadowcast': 40}, 'talents': ['Wraith Path: Twisted Puppets']}`
- **추가 정보**: While buffed, your Puppets will gain an orange swirling aura. On proc, this buffs all currently alive Puppets and all Puppets that spawn within the next 10 seconds. The following abilities and Talents proc Explosive Rage: Explosive Finish, Emperor Flame, Scorchblood, The Final Act, and the Detonation enchant.

### Moths to a Flame `[Common]`
- **설명**: Your Twister Puppets now home towards burning enemies. | **요구조건**: `{'stats': {'Flamecharm': 40, 'Shadowcast': 40}, 'talents': ['Wraith Path: Twisted Puppets']}`
- **추가 정보**: Puppets will now home in on targets who are burning with either of Twisted Puppets' burn types. When a Puppet gets close to a burning target it speeds up.

### Audacity `[Advanced]`
- **설명**: Once you've brought down your prey, instill fear into all those who would separate you from claiming it. Charmed or nearby enemies will fear for longer. Nearby allies gain a 10% damage buff (40s). | **요구조건**: `{'stats': {'Charisma': 100, 'Strength': 50}}`
- **추가 정보**: Applies true stun to nearby enemies when you start a manual execution on a humanoid target. 25 second cooldown. The buff duration will be reduced by 0.1 seconds for every point of Charisma and Strength you are below Audacity's requirements, capping at a minimum 35 second duration with 75 Charisma and 25 Strength.

### No Survivors `[Common]`
- **설명**: Your allies and yourself execute faster when affected by Overcharm. | **요구조건**: `{'stats': {'Charisma': 80, 'Strength': 45}}`
- **추가 정보**: Reduces grip time by 0.5 seconds (16.67% faster).

### Denial Repulse `[Rare]`
- **설명**: You now emit a delayed burst of flames after coming close to death. | **요구조건**: `{'stats': {'Willpower': 40, 'Flamecharm': 40}, 'mantras': ['Flame of Denial']}`
- **추가 정보**: When Flame of Denial protects you, release an explosion around you. This deals 20 Flamecharm damage with 5 Flamecharm scaling. This cannot be parried nor dodged, but can be blocked, dealing 5 posture damage. Has a windup of 0.6s.

### Undying Flame `[Rare]`
- **설명**: Your Graceful Flame burns brightly even underwater. Those that gather around it are soothed and regain sanity. | **요구조건**: `{'stats': {'Willpower': 40, 'Flamecharm': 40}, 'mantras': ['Graceful Flame']}`
- **추가 정보**: Graceful Flame can be casted in the First Layer. It cannot be used in the Diluvian Mechanism or Depths Trials, however. Graceful Flame passively restores sanity and health to those around it.

### Surge Path: Unstable Capacitor `[Common]`
- **설명**: Your lightning no longer applies Shock, instead apply Surge. At maximum stacks of Surge, your opponents will Overload, sending arcs of lightning in every direction. | **요구조건**: `{'stats': {'Thundercall': 40}}`
- **추가 정보**: Turns your Thundercall abilities blurple. Shock is replaced with Surge Rods, a stacking status effect that Overloads upon applying five Rods and then landing an attack that would apply a sixth, consuming all of the Rods. Each Rod has an individual 30 second duration. Surge Overloads deal 2.5 Thundercall damage per Rod with 5 Thundercall scaling to Overloaded target, gaining 0.0125 damage per Thundercall investment, and 2 Thundercall damage per Rod in an AoE that does not hit the Overloaded target.

### Battery Sapper `[Common]`
- **설명**: If your Human Battery targets have Ether, it will drain their Ether to help pay for your Mantras. 10s cooldown. | **요구조건**: `{'stats': {'Thundercall': 60, 'Shadowcast': 25}, 'talents': ['Surge Path: Unstable Capacitor']}`

### Catalytic Strike `[Common]`
- **설명**: Posture breaking an enemy will Overload their Surge stack. | **요구조건**: `{'stats': {'Thundercall': 50}, 'talents': ['Surge Path: Unstable Capacitor']}`

### Closed Circuit `[Common]`
- **설명**: Surge Overloads that fail to arc to other opponents will deal additional damage to the Overloaded enemy. | **요구조건**: `{'stats': {'Thundercall': 50}, 'talents': ['Surge Path: Unstable Capacitor']}`
- **추가 정보**: Adds 5 Thundercall damage with 5 Thundercall scaling to the Overload, gaining 0.025 damage per Thundercall damage. This is a flat value that does not depend on Rod count.

### Human Battery `[Common]`
- **설명**: When you are out of Ether, convert the Surge stacks of nearby enemies into Ether to pay the cost of your Mantras. | **요구조건**: `{'stats': {'Thundercall': 60}, 'talents': ['Surge Path: Unstable Capacitor']}`
- **추가 정보**: Each Rod equates to 10 Ether. Works on Rods that weren't applied by you, but does not work on Rods applied to you.

### Flashboil `[Common]`
- **설명**: Landing Ice/fire attacks on burning/chilled enemies extinguishes the flame and generates steam. | **요구조건**: `{'stats': {'Flamecharm': 30, 'Frostdraw': 30}}`
- **추가 정보**: Steam deals 2 typeless damage per tick, at 6 ticks per second. Steam cannot be blocked nor parried.

### Boiling Point `[Common]`
- **설명**: Using a fire mantra near your own steam cloud detonates it. | **요구조건**: `{'talents': ['Flashboil']}`
- **추가 정보**: Deals 10 typeless damage. This cannot be parried nor blocked. Procs when you hit the Steam cloud with your Flamecharm Mantra, meaning your opponent can parry your Mantra and this will still proc.

### Action Surge `[Common]`
- **설명**: Adrenaline Surge now increases your swing speed by 0.04 for its duration. | **요구조건**: `{'stats': {'Agility': 70}}`
- **추가 정보**: Both this and Vigil's Grace are applied before Lightning Cloak's swing speed multiplier.

### Bear Trap `[Common]`
- **설명**: Landing a hit with your critical against an opponent makes your opponent unable to jump for a duration. Also slows your opponent and procs Sluggish on PvE. | **요구조건**: `{'stats': {'Strength': 20, 'Agility': 20}}`
- **추가 정보**: Affected targets cannot jump for 4 seconds. Targets gain 6 seconds of Bear Trap immunity.

### Blade Dancer `[Common]`
- **설명**: Landing a Basic Attack removes your roll cooldown. | **요구조건**: `{'stats': {'Agility': 25}}`

### Cut to the Chase `[Rare]`
- **설명**: Air Counter damage scaling is largely increased. Landing an Air Counter now initiates an uppercut. Deal 5% more damage to PvE enemies in the air. | **요구조건**: `{'stats': {'Agility': 60}}`
- **추가 정보**: Adds 10 True damage to your Air Counter. The damage bonus will be lessened if you do not meet the Talent's requirements.

### Speed Demon `[Rare]`
- **설명**: Your attacks now inflict a reduced-strength bleed while you have a speed boost. 1s cooldown. | **요구조건**: `{'stats': {'Agility': 25}}`
- **추가 정보**: Speed Demon's bleed deals 2.5% of your weapon's scaled damage every 0.3s, three times. This totals to 7.5% of your weapon's scaled over a 0.9 second period. Bleed deals typeless damage.

### Spinning Swordsman `[Common]`
- **설명**: Running attacks do +15% extra damage when you have a speed boost. | **요구조건**: `{'stats': {'Agility': 20}}`

### Oath: Visionshaper `[Oath]`
- **설명**: You vow to only see that which you wish to see. Reality itself is malleable, pliable to your deft hands.  | **요구조건**: `{'stats': {'Charisma': 50}, 'objectives': ["Complete Aelita's Encounter or Carnival of Hearts, bring a Dark Feather to Surge."]}`

### Cheap Trick `[Oath]`
- **설명**: When hit below half health briefly disappear, leaving behind an illusion clone to keep your enemy occupied for a short duration. Briefly disappear after knocking an enemy. | **요구조건**: `{'talents': ['Oath: Visionshaper'], 'or': [{'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Being hit while under half HP grants I-frames and turns you invisible for a very short duration. 60s CD. Knocking an opponent turns you invisible for 2.5 seconds with no I-frames.

### Reality Shift `[Oath]`
- **설명**: Command the closest conjured servant to attack their hallucinating target, either using a Critical Attack or a Mantra. | **요구조건**: `{'talents': ['Oath: Visionshaper'], 'or': [{'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Your last used Mantra or critical attack will be stored in your clones when you summon them. Using the Reality Shift Talent tool or hotkey will perform the stored action.

### Shared Mimicry `[Oath]`
- **설명**: The servants you have conjured will imitate your actions when you Swing/Block/Parry/Jump. | **요구조건**: `{'talents': ['Oath: Visionshaper'], 'or': [{'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Your clones will also Vent when you Vent. This can trigger even if you do not have Tempo or if you press G while in an animation.

### Encore `[Rare]`
- **설명**: Your Sing will stun opponents who are already charmed. | **요구조건**: `{'stats': {'Charisma': 40}, 'mantras': ['Sing']}`
- **추가 정보**: Applies 0.4s of true stun. Doesn't affect allies.

### Vow of Mastery `[Common]`
- **설명**: The Vow of Mastery grants the Master the power to command their Subject. To initiate a vow you must ask the other player if they'd like to make the vow. e.g. "wanna make a vow of mastery?" | **요구조건**: `{'stats': {'Charisma': 20}}`
- **추가 정보**: Players who take the vow are considered allies with their master and others who take the vow. Commands Given: "Sleep", "Drop", "Run", "Eat", "Say (Text)", "Use", "Locate", and "Leech" at base. "Fight" and "Sacrifice" at 50 Charisma, "Return" at 60 Charisma, and "Explode" at 75 Charisma.

### Command: Live `[Common]`
- **설명**: Once per hour, command a servant to defy all odds and obey your command - live. | **요구조건**: `{'stats': {'Charisma': 75}, 'talents': ['Vow of Mastery']}`
- **추가 정보**: Fully heals your Servant if they are below 40% health. The cooldown of this Command scales on your Charisma investment.

### Command: Summon `[Advanced]`
- **설명**: Command your servant to obey your summons and appear before you no matter the distance. | **요구조건**: `{'stats': {'Charisma': 80}, 'talents': ['Vow of Mastery']}`
- **추가 정보**: Teleports the subject to the master regardless of distance. Teleportation takes 10 seconds to complete, and any hit will cancel it. 30 second cooldown for the Master, 2 minute cooldown for the Servant.

### Chronostasis `[Rare]`
- **설명**: Landing a Basic Attack or Critical puts the target's Resonance on cooldown for a short duration, while also applying Ether Sunder to PvE opponents.  | **요구조건**: `{'stats': {'Power': 13}}`
- **추가 정보**: On hit, apply a 13 second Resonance cooldown. This cannot proc if their Resonance is already on cooldown.

### Conditioned Swimmer `[Common]`
- **설명**: You lose less hunger and thirst while swimming.

### Brutal Momentum `[Common]`
- **설명**: [Heavy Weapons] Successfully dodging will give you hyperarmour on your next swing. | **요구조건**: `{'stats': {'Heavy Weapon': 50}, 'weaponType': 'Heavy Weapon'}`

### Matador `[Common]`
- **설명**: Deal +20% more damage to human enemies with hyperarmor. | **요구조건**: `{'stats': {'Strength': 20, 'Agility': 5}}`

### Showstopper `[Rare]`
- **설명**: When an enemy would roll through one of your physical attacks, stomp the ground, dazing anyone nearby. Removes speed buffs from target upon landing. | **요구조건**: `{'stats': {'Strength': 40}}`

### Switchblade `[Advanced]`
- **설명**: You can now utilize Dagger Talents when not wielding a dagger. | **요구조건**: `{'stats': {'Light Weapon': 50}, 'or': [{'stats': {'Medium Weapon': 50}}, {'stats': {'Heavy Weapon': 50}}]}`
- **추가 정보**: This applies to all weapon types, applying the effects of Dagger Talents to any equipped weapon.

### Warrior's Swing `[Common]`
- **설명**: [Heavy Weapons] Reduces incoming damage by 5% if hit during Heavy swing hyperarmor. | **요구조건**: `{'stats': {'Heavy Weapon': 30}}`

### Haunted Gale `[Common]`
- **설명**: Landing 3 Galebreathe Mantras without whiffing calls forth a Haunted Phantom. The Phantom will attack alongside you for the next 8s before dissipating. | **요구조건**: `{'stats': {'Power': 8, 'Galebreathe': 40}}`
- **추가 정보**: On proc, gain the Haunted status effect, spawning ghosts that attack your opponent every time you land a Mantra. Ghosts have 15 base damage with 5 Galebreathe scaling. Having Gale Wisp active increases the duration of Haunted by 3 seconds. If you have Apparitions, landing a Galebreathe Mantra while having the Haunted Gale status effect will create an Apparition instead while non-Galebreathe Mantras will summon Haunted Gale's Ghosts like normal.

### Agility Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your agility to its fullest. | **요구조건**: `{'stats': {'Agility': 75}, 'objectives': ['Speak to Windrunner']}`
- **추가 정보**: Removes the 75 investment cap on the Agility Attribute. The requirements to obtain this Talent will be increased to 77 or 78 if your Aspect has increased Agility on spawn, though this limitation will be removed if you have the Multifaceted Echo Unlock. The quest requirement for this Talent will be removed if you've obtained it previously on your account.

### Ash Ember `[Common]`
- **설명**: The more wither your opponent has, the more damage your burn deals. | **요구조건**: `{'stats': {'Weapon': 90, 'Flamecharm': 90}}`
- **추가 정보**: At 90 FLM 90 WPN you gain a 0.0175 burn damage increase per 1 point of wither. This has very slight Flamecharm and Weapon scaling.

### Brassneck `[Common]`
- **설명**: Knocking an enemy grants you 20% damage resistance for 15 seconds. | **요구조건**: `{'stats': {'Strength': 30, 'Fortitude': 35}}`
- **추가 정보**: Works on non-humanoid monsters, applying the damage reduction after they die.

### Careful Handling `[Quest]`
- **설명**: Reduce your chances of dropping ingredients on death. | **요구조건**: `{'quests': ["Suri's Flower"]}`

### Dragon's Song `[Common]`
- **설명**: Using a mantra after an uppercut grants ether.
- **추가 정보**: Grants +20 Ether on proc. 2 second cooldown.

### Full Reset `[Common]`
- **설명**: Knocking an enemy resets your resonance cooldowns. This effect has a 60 second cooldown. | **요구조건**: `{'stats': {'Power': 16}, 'objectives': ['Obtain a Resonance']}`
- **추가 정보**: Also works on non-humanoid monsters, resetting your Resonance cooldown after they die.

### Gourmand `[Common]`
- **설명**: Your hunger and thirst gain from eating is increased. | **요구조건**: `{'stats': {'Power': 5}}`
- **추가 정보**: Increases hunger and thirst gain by 20%.

### Heavy Haul `[Common]`
- **설명**: Enemies who carry you move significantly slower. Take slightly less posture damage from large enemies. Takes one to know one. | **요구조건**: `{'stats': {'Strength': 15}}`

### Martyr `[Common]`
- **설명**: When you're knocked Unconscious, enemies gain less health and posture, and allies around you are granted Martyrdom for 20s | **요구조건**: `{'stats': {'Power': 3}}`
- **추가 정보**: Martyrdom grants a +20% damage and damage reduction buff to your allies. Enemies who knock you restore only half of the posture and health they would normally obtain (50% -> 25%).

### Polite Awakening `[Common]`
- **설명**: Upon recovering from being Unconscious, your health is restored up to a minimum of 15% of your max health.

### Ready or Not `[Common]`
- **설명**: The first attack to hit you while out of combat has its damage cut in half. | **요구조건**: `{'stats': {'Fortitude': 20}}`

### Replenishing Knockout `[Common]`
- **설명**: You gain more health and posture from downing enemies. | **요구조건**: `{'stats': {'Power': 3}}`
- **추가 정보**: Knocking enemies will replenish 1.5x more of your health and posture (50% -> 75%).

### Treefelling Blow `[Quest]`
- **설명**: You can collect lumber from the trees you fell with your fists. It's only natural.
- **추가 정보**: Allows you to gain Wood when you destroy trees with Strong Left.

### Assassin's Strike `[Weapon]`
- **설명**: Your Rapid Slashes now deals twice the amount of damage. | **요구조건**: `{'weapon': 'Silver Dagger'}`
- **추가 정보**: Doubles the base damage of Rapid Slashes.

### Battle Frenzy `[Weapon]`
- **설명**: The grip on your weapon tightens, reduce the posture of all mantras you block with this effect scaling with the number of combat tags you have on your character. | **요구조건**: `{'weapon': "Master Hawk's Handaxe"}`
- **추가 정보**: This reduces the posture damage of incoming Mantras by 1 per hit, per combat tag you have. If you have more combat tags than the Mantra does posture damage, this can go into the negatives and your posture will be restored instead.

### Belief `[Weapon]`
- **설명**: Your medium weapon mantras now deal extra damage based on how much Willpower you have. | **요구조건**: `{'weapon': 'Worshipper Longsword'}`
- **추가 정보**: All of your Medium Weapon Mantras gain a second damage instance that scales directly on your Willpower investment and deals true damage. This deals 0.15 damage per 1 Willpower investment, up to 15 damage at 100 Willpower. This has no cooldown. Having One With Flame active adds an additional +0.05 damage to Belief, for every 1 Flamecharm investment you have.

### Blitz `[Weapon]`
- **설명**: Increase how quick you release your Prominence Draw. | **요구조건**: `{'weapon': 'Forgotten Gladius'}`
- **추가 정보**: Decreases Prominence Draw's windup by 0.1s (from 0.55s to 0.45s).

### Blood Drinker `[Weapon]`
- **설명**: Recover health on hit. When landing a critical, deal 30 bleed damage over 5 seconds. | **요구조건**: `{'weapon': 'Bloodbane'}`
- **추가 정보**: Restores 4% of the user's maximum health upon landing M1 attacks. The "bleed" is a unique damage over time status effect that is not bleed. This deals 6 damage per tick and ticks 5 times over 5 seconds. This can proc on Motif-given critical attacks. If you are knocked during the duration of this "bleed" effect, you will be instantly gripped.

### Bulwark Breaker `[Weapon]`
- **설명**: Increase the size of your Pressure Blast, with the last hit of it dealing increased posture damage. Your Pressure Blast is also now unparryable. | **요구조건**: `{'or': [{'weapon': 'Steel Maul'}, {'weapon': 'Alloyed Steel Maul'}]}`
- **추가 정보**: Increases the AoE and range of your Pressure Blast. The final hit of your Pressure Blast deals 3x the posture damage (from 12 to 36), increasing the total posture damage of the Mantra from 36 to 60.

### Careful Stance `[Weapon]`
- **설명**: Gain a bit more autoparry frames on successful parries. | **요구조건**: `{'weapon': 'Apprentice Rapier'}`

### Clutch Recovery `[Weapon]`
- **설명**: When at 30% health or below, every time you land a light attack or critical hit heal 1%. | **요구조건**: `{'weapon': 'Canor Fang'}`
- **추가 정보**: If you are at or below 30% of your maximum health, heal 1% of your maximum health upon landing any weapon attack.

### Corporeal Dissolution `[Weapon]`
- **설명**: Applies Wither on any weapon attack that drains Ether, and scales on the amount of Ether drain. | **요구조건**: `{'weapon': 'Black Death'}`
- **추가 정보**: Caps at 30 Wither damage per proc.

### Cruel Counter `[Weapon]`
- **설명**: When using your initial charge up on your Krulian Knife, if you interrupt someone's attack with it apply Cruel Counter on them, massively increasing the damage they take from your critical attacks. | **요구조건**: `{'weapon': 'Krulian Knife'}`
- **추가 정보**: If you interrupt someone's attack with the shock from your Krulian Charge critical, apply the Cruel Counter status effect to your opponent, increasing all damage taken by critical attacks for 20 seconds. This grants a 40% damage buff to all critical attacks (including those that aren't Krulian Knife's), bypassing the damage modifier caps.

### Curved Edge `[Weapon]`
- **설명**: Your light weapon mantras now gain 30% more chip. | **요구조건**: `{'weapon': "Nemit's Sickle"}`

### Expeditionary Evasiveness `[Weapon]`
- **설명**: The design of this rapier allows you to much more swiftly attack in tandem with your mantras, giving Agility mantras you use +3 levels in all stats, even bypassing the level cap. | **요구조건**: `{'weapon': "Inquisitor's Thorn"}`
- **추가 정보**: Your Agility Mantras gain 3 Mantra levels, bypassing the level 5 cap. This is not displayed on the Mantra tooltip. Jetstriker Mantras are unaffected by this.

### Expeditious Combo `[Weapon]`
- **설명**: Landing an uppercut will grant a buff to your Onslaught for 15 seconds, using Onslaught during this time will massively increase the speed of it. | **요구조건**: `{'weapon': 'Iron Birch'}`
- **추가 정보**: Passively increases the speed of your Onslaught. After landing a basic attack uppercut, gain the Expeditious Combo status effect for 15 seconds, displayed on the cooldown indicator. Casting Onslaught while you have this status effect will massively increase its speed, consuming the status effect in the process. This has no cooldown, but must be manually refreshed every time you use it.

### Extended Trauma `[Weapon]`
- **설명**: Successful light attacks and criticals on your opponent now also gives them a bit of posture. | **요구조건**: `{'weapon': 'Morning Star'}`
- **추가 정보**: Deals 3 posture damage to non-blocking opponents on M1, and 10 posture damage on critical. This cannot posture break, and this does not benefit from posture damage modifiers.

### Finishing Slay `[Weapon]`
- **설명**: If you land a critical attack while also having stacks from the Chain of Perfection talent, consume all those for a massive damaging attack. This works on other players as well. | **요구조건**: `{'weapon': 'Messer'}`
- **추가 정보**: Consumes all of your Chains of Perfection stacks for a secondary instance of damage on your critical. This deals 7 typeless damage per Chain of Perfection stack in PvP, or 166 typeless damage per stack in PvE. The first 5 hits that normally do not grant stacks will contribute to this, allowing you to deal 150 PvP damage or 3.5k PvE damage at maximum Chain stacks. This can be buffed, but it is not considered as a weapon attack, limiting buffing options. Finishing Slay has no cooldown, allowing multi-hit criticals to deal massive damage in PvE.

### Forced Fulfilment `[Weapon]`
- **설명**: Your Metal Greatsword now has Metal Fakeout as its critical attack. Landing a critical attack using your Metal Greatsword attaches a heavy rod onto your opponent, heavily slowing them. | **요구조건**: `{'weapon': 'Metal Greatsword'}`
- **추가 정보**: The Metal Fakeout critical only works while you are in range of a target. Additionally, this critical applies Bleed and counts as a weapon attack, not a Mantra. The rod applies a 52.5% slow for 15 seconds.

### Fortify `[Weapon]`
- **설명**: Slow down your movement in exchange for fortifying your defenses. | **요구조건**: `{'weapon': 'Rimebreakers'}`
- **추가 정보**: Grants a Talent tool that grants 15% damage reduction at the cost of reducing your movement speed by 36%.

### Phantom `[Weapon]`
- **설명**: For the next 5 seconds, your next basic attack bypasses block after landing a crit. [45 second CD] | **요구조건**: `{'weapon': 'Withered Phantomcleave'}`
- **추가 정보**: Your weapon attacks that bypass block apply shaky block.

### Pierce Through `[Weapon]`
- **설명**: Remove the autoparry frames the first hit of your base spear critical has. | **요구조건**: `{'or': [{'weapon': 'Ritual Spear'}, {'weapon': 'Ritual Sacrifice'}]}`
- **추가 정보**: The default spear critical attack no longer cancels if the first hit is parried. Additionally, parrying the first hit of this critical does not provide autoparry frames.

### Pugnacious `[Weapon]`
- **설명**: Become stronger the more you are combat tagged. Gain even more strength whenever you grip a player. | **요구조건**: `{'weapon': 'Warmonger'}`
- **추가 정보**: Gain various stacking buffs scaling on the amount of combat tags you have. Gain a further damage buff upon executing a player. On basic attack, gain +10% to the following stats: damage, posture damage, elemental damage resistance, physical damage resistance, chip damage, and speed boost per combat tag you have. The damage, posture damage, and chip damage effects ignore the modifier caps but cap at +30%. The resistance bonuses are multiplicative to other sources of their respective resistance types. The speed boost has no cap in effectiveness.

### Punishing Riposte `[Weapon]`
- **설명**: When parrying a guardbreak, enhance your critical for the next 15 seconds. If you land your crit on your opponent's block while it is enhanced, immediately guardbreak your opponent. | **요구조건**: `{'weapon': 'Crucible Rapier'}`

### Rat's Spirit `[Weapon]`
- **설명**: Each hit of your critical will deal an extra 10 true damage per combat tag whenever you are combat tagged by 2 or more people. | **요구조건**: `{'weapon': "Champion's Dagger"}`
- **추가 정보**: Being combat tagged by 2 or more players will cause your critical attack to deal an additional 10 true damage per hit. This scales on how many combat tags you have, gaining +10 damage per.

### Rosen's Technique `[Weapon]`
- **설명**: If you use Tactical Reload, Rosen's Peacemaker has 45 seconds less off its cooldown. | **요구조건**: `{'weapon': "Rosen's Peacemaker"}`
- **추가 정보**: Reduces the cooldown of Tactical Reload by 45 seconds; from 90 seconds to 45.

### Sable Winds `[Weapon]`
- **설명**: You can now Inhale Shadowcast mantras. Aftercut effects now drain a small amount of ether based on the damage they deal. | **요구조건**: `{'weapon': 'Eyes of Ethiron'}`
- **추가 정보**: Inhale bonuses now apply to Shadowcast Mantras as well.

### Sacrificial Boon `[Weapon]`
- **설명**: Sacrifice 5 knowledge to activate Blessing, giving you a random blessing from Navae. | **요구조건**: `{'weapon': 'Ritual Sacrifice'}`
- **추가 정보**: Grants a Talent tool that consumes 5 KnowledgeSprite on use to grant the user a random buff within a set pool. This has a 0.5 second cooldown, potentially allowing you to stack the buffs. Potential buffs are: 20% damage buff, hyperarmor for 10 seconds, instantly heal 50 health, thirst restoration, stomach restoration, or a speed boost for 10 seconds.

### Soar `[Weapon]`
- **설명**: Retain full walkspeed while using your crit. | **요구조건**: `{'weapon': 'Withered Gale Pale'}`
- **추가 정보**: This allows you to retain your full momentum during your weapon critical. This Talent will be disabled if you equip a Motif onto the Withered Gale Pale.

### Sovereign's Counter `[Weapon]`
- **설명**: Improve the efficiency of every counter you use. This effect becomes stronger for Punishment if you have the Riot Breaker talent. | **요구조건**: `{'weapon': "Inquisitor's Greatsword"}`
- **추가 정보**: Punishment has its reflected damage output increased by 12.5% additively, meaning at level 5 you can reflect 112.5% of someone's damage on top of the base damage. If the Authority Commander Outfit is equipped, the longevity of the attack window on your Punishment is increased by 3x; from 20 seconds to a full minute. Prediction's active frames are increased slightly. Curse of the Unbidden has its posture restoration increased by 10%, restoring 40% of your posture. Payback has its active counter frames increased by 0.7 seconds.

### Spinal Splinter `[Weapon]`
- **설명**: Landing a backstab with your critical deals 15 extra true damage. | **요구조건**: `{'weapon': 'Halberd'}`
- **추가 정보**: If your critical attack hits your opponent's back, it will gain an secondary damage instance that deals 15 true damage.

### Static Beatdown `[Weapon]`
- **설명**: Landing a Thundercall mantra electrifies the metal in your Cestus for 8 seconds, extending how long your opponents are stuck in shaky block based on your total Thundercall investment. | **요구조건**: `{'weapon': 'Legion Cestus'}`
- **추가 정보**: Shaky block duration scales on your Thundercall investment, increasing by +0.004s for every point in Thundercall.

### Subzero `[Weapon]`
- **설명**: Landing a running attack inflicts your opponent with a deep freeze. Additional light hits after the opponent thaws out will briefly slow them as well. | **요구조건**: `{'weapon': 'Winter Rifle'}`

### Swift Strike `[Weapon]`
- **설명**: Land a light attack behind your opponent to enhance your next critical, allowing you to teleport behind your opponent and strike them. This enhanced critical also procs assassination talents. | **요구조건**: `{'weapon': 'Big Brother'}`
- **추가 정보**: On proc, you gain the Swift Strike status effect indefinitely. This effect will be consumed when you use your critical. The teleport has a range limit. 20 second cooldown.

### True Seraph Slash `[Weapon]`
- **설명**: Landing the first hit of your critical attack enhances your next critical, giving you access to the Angels' spear smite ability. Having Starkindred Wings out or Angel's Guise adds 1 bolt to your enhanced crit. | **요구조건**: `{'weapon': 'True Seraph Spear'}`
- **추가 정보**: This deals 0.75x of your weapons scaled damage as typeless damage per hit (4 at base). Having Angel's Guise or Starkindred wings out adds an additional hit. Having both adds a second additional hit and summons an allied Sworn Angel.

### True Shatter `[Weapon]`
- **설명**: Landing a critical shatters your opponent, ridding them of their speed debuffs and dealing true damage scaling off how slow they were. | **요구조건**: `{'weapon': 'Coldpoint'}`
- **추가 정보**: Deals 5 true damage per slow debuff.

### Vital Wound `[Weapon]`
- **설명**: Uppercutting your opponent punctures their lungs, slowing their rate of posture recovery by 30% for 30 seconds. | **요구조건**: `{'weapon': "Acheron's Warspear"}`
- **추가 정보**: Uppercutting your opponent applies the Vital Wound status effect, reducing their passive posture recovery by 30% for 30 seconds. This has no cooldown, but it cannot be refreshed or reapplied while it's active.

### Actions Speak Louder `[Equipment]`
- **설명**: Your Critical Attack cooldown is 20% shorter, but your Resonance cooldown is 20% longer. In areas where your Resonance is suppressed, reduce your cooldown by 10% instead. | **요구조건**: `{'equipment': "Warmaster's Medallion"}`
- **추가 정보**: In 1v1 Chime of Conflict, your critical cooldown is reduced by 10% instead.

### Alloyed Soles `[Equipment]`
- **설명**: Reduces the duration of Knockdown applied to you. | **요구조건**: `{'equipment': 'Ossified Phalanx Boots'}`
- **추가 정보**: Reduces knockdown duration by 75%.

### Already Dead `[Equipment]`
- **설명**: You take reduced damage from abilities with a health cost. | **요구조건**: `{'equipment': 'Deepscorn Casque'}`
- **추가 정보**: Removes the self damage from Deepspindle's running critical. Reduces the self damage from Shade Devour, Flame Within (on cast, NOT the burn ticks), Rush Hour, Shadow Travel, Electrify, and 'Poison' Corrupt Resonance downside. Reduces the self Wither gain from Symbiotic Link and the 'Wither' Corrupt Resonance downside.

### Angel's Guise `[Equipment]`
- **설명**: You resemble one of the Sworn Angels. | **요구조건**: `{'or': [{'equipment': 'Hollow Angel Mask'}, {'equipment': 'Sworn Angel Mask'}]}`
- **추가 정보**: Grants immunity to the Watcher's Watcher Gaze attack, preventing Sanity loss, vision distortion, and the spawning of Hollow Angel(s). Additionally grants unique dialogue with the Watchers.

### Art of the Deal `[Equipment]`
- **설명**: Your rapport with merchants gives you lower prices! | **요구조건**: `{'equipment': 'Aristocrat Coat'}`
- **추가 정보**: Reduces the purchase price of items by 10%.

### Blinded `[Equipment]`
- **설명**: Your vision is obscured by something. Somehow, you feel safer. You remember the warmth of your youth. | **요구조건**: `{'or': [{'equipment': 'Blindfold'}, {'equipment': "Inquisitor's Visor"}]}`
- **추가 정보**: Makes everything darker and creates fog at long distances. Grants immunity to the Flame Blind and Gaze Mantras.

### Blood Convergence `[Equipment]`
- **설명**: Receive 10% more healing from all healing sources when you have temp health. | **요구조건**: `{'equipment': 'Regenerative Earrings'}`

### Blood Pact `[Equipment]`
- **설명**: Gain 50 bonus temporary health whenever you knock/kill an enemy. | **요구조건**: `{'equipment': 'Regenerative Pendant'}`

### Blood Necrosis `[Equipment]`
- **설명**: Your bloodless gems heal 33% less than usual. | **요구조건**: `{'equipment': "The No-Life King's Crown"}`
- **추가 정보**: You will now need a scaled damage of 75 to hit the regular Bloodless Gem heal cap of 15.

### Blood Plague `[Equipment]`
- **설명**: For every light attack you land, add one Blood Plague stack on your opponent. Landing a Critical Attack converts all Blood Plague stacks into temporary health but missing the attack loses them. | **요구조건**: `{'equipment': 'Necrotic Mask'}`
- **추가 정보**: M1s apply stacks of Blood Plague. On critical, all Blood Plague stacks will be consumed to grant Temporary Health if your critical attack lands, with the amount of Temporary Health given scaling on the stacks of Blood Plague. The stacks of Blood Plague will be consumed regardless of if your critical attack lands, however.

### Brute Strength `[Equipment]`
- **설명**: Your vent is replaced with a ground slam attack that knocks back enemies. | **요구조건**: `{'equipment': "Imperator's Fury"}`
- **추가 정보**: Deals 35 Blunt damage with 20 Posture damage. This cannot be buffed through damage modifiers. Increases your Vent's windup from 0.25s to 0.5s.

### Coldseep Reactor `[Equipment]`
- **설명**: By cultivating the localized chemosynthetic microorganisms within the Depths and utilizing them as a power source, your helm thrums with a protective field of static electricity and heat. | **요구조건**: `{'equipment': 'Grand Fisher Helm'}`
- **추가 정보**: You can no longer gain parasites while in the Second Layer.

### Cosmic Connection `[Equipment]`
- **설명**: All celestial and astral related abilities are buffed. | **요구조건**: `{'equipment': 'Celestial Boots'}`
- **추가 정보**: Increases Astral's damage buff in PvE from +20% to +25%.

### Crippling Impact `[Equipment]`
- **설명**: Landing a critical  on someone while Wrath Gem is active disables their vent for a few seconds. | **요구조건**: `{'equipment': 'Reinforced War Plate'}`
- **추가 정보**: The duration of this effect scales on your Strength investment, being 2 seconds + 0.015 seconds per point of Strength. This lasts for 3.5 seconds at 100 Strength.

### Destructive Yell `[Equipment]`
- **설명**: Your Ardour Screams now break campfires around you and have a larger AoE. | **요구조건**: `{'equipment': 'Ascended Outlaw Mask'}`
- **추가 정보**: Your Ardour Scream destroys all campfires within its range.

### Diver's Resilience `[Equipment]`
- **설명**: You can parry unparryable attacks from giant monsters, but due to the heft of the plate, you have slightly reduced speed. | **요구조건**: `{'equipment': 'Grand Fisher Plate'}`
- **추가 정보**: You can now parry certain NPC attacks that are normally unparryable. 10 second cooldown.

### Drop Dead `[Equipment]`
- **설명**: Take less damage when you are crouching. | **요구조건**: `{'equipment': 'Vaporfrost Earrings'}`

### Elegy of Light `[Equipment]`
- **설명**: The Unspoken Vow of the Waking God resonates through you, if briefly. Protects you from the effects of Deep Gems for 3 minutes and provides you Gem Enhancement. Remains dormant until you take the life of an equal. | **요구조건**: `{'equipment': "Lightkeeper's Medallion"}`
- **추가 정보**: On use, Deep Gems cannot have their effects proc on you and your Deem Gems have increased effectiveness in PvE for 3 minutes. This ability requires you to kill a player of equal or higher level or a boss to recharge its effect.

### Enforcer's Strength `[Equipment]`
- **설명**: Your enemies recover 20% less posture on parry. | **요구조건**: `{'equipment': 'Hardened Enforcer Plate'}`

### Enforcer's Technique `[Equipment]`
- **설명**: Your flourishes deal 35% more damage. | **요구조건**: `{'equipment': 'Hardened Enforcer Boots'}`

### Ether Adeptness `[Equipment]`
- **설명**: Your mantras now deal extra chip. | **요구조건**: `{'equipment': 'Ether Empowered Earrings'}`
- **추가 정보**: Grants 5% chip damage.

### Ether Emergency `[Equipment]`
- **설명**: When you get hit below 25% health, exhaust all of your ether to gain a flat health boost (healing scales of total max ether). You are briefly unable to cast Mantras. | **요구조건**: `{'equipment': 'Bluestone Pauldrons'}`
- **추가 정보**: On proc, restore health equal to 15% of your maximum Ether. 5 minute cooldown.

### Ether Tension `[Equipment]`
- **설명**: Deal bonus true damage whenever you guardbreak an opponent with a mantra. | **요구조건**: `{'equipment': 'Ether Imbued Earrings'}`
- **추가 정보**: Deals 10 true damage.

### Ether Pinpoint `[Equipment]`
- **설명**: Mantras that have Might Gem on them now ignore fully ignore the posture bonus from shields. | **요구조건**: `{'equipment': 'Ascended Outlaw Robes'}`

### Fatal Strike `[Equipment]`
- **설명**: Landing a guardbreak with a strength mantra that has a Wrath Gem on it devastates your opponent, slowing them down. | **요구조건**: `{'equipment': 'Reinforced War Helmet'}`
- **추가 정보**: Applies a 50% slow for 5.5 seconds. 10 second cooldown. This deals an extra 15 true damage on proc if you are using the full Reinforced War set.

### Featherfall `[Equipment]`
- **설명**: Prevents falls from damaging you. After sufficient damage has been resisted, the pendant will go inactive and require time to recharge. | **요구조건**: `{'equipment': 'Tiran Pendant'}`
- **추가 정보**: Nullifies fall damage. Once 255 fall damage has been nullified, this will go on a 2 minute cooldown, disabling its benefits.

### Flashwind `[Equipment]`
- **설명**: Anytime you proc Air Pressure or Overcharge, give yourself the ability to have enhanced dashes again for a few seconds. | **요구조건**: `{'equipment': 'Specialist Boots'}`
- **추가 정보**: After using a Gale or Lightning dash, gain the Flashwind status effect for 3 seconds, allowing you to perform Flashwind dashes.

### Focused Strikes `[Equipment]`
- **설명**: All criticals deal 15% more posture damage. | **요구조건**: `{'equipment': 'Gale Enhanced Beads'}`

### Footwork Mastery `[Equipment]`
- **설명**: Landing a critical gives you an immense speed boost for 10 seconds. | **요구조건**: `{'equipment': 'Gale Enhanced Cowl'}`
- **추가 정보**: The speed boost lasts 15 seconds despite what the description states. 45 second cooldown.

### Force Your Way `[Equipment]`
- **설명**: You can parry unparryable attacks from giant monsters, at the cost of armor durability. | **요구조건**: `{'or': [{'equipment': 'Ignition Gauntlets'}, {'outfit': 'Ignition Deepdelver'}]}`
- **추가 정보**: You can now parry certain NPC attacks that are normally unparryable. On proc, your armor will be drained, with the amount of armor lost being based on the damage the attack would normally deal. This Talent does not work if you have no armor durability.

### Grotesque Resilience `[Equipment]`
- **설명**: You take reduced damage from 'Damage over Time' effects. | **요구조건**: `{'equipment': 'Parasol Planter'}`
- **추가 정보**: Reduces burn damage by 50%. Reduces Flame Within's burn and bleed damage by 25%.

### Heartwing Beat `[Equipment]`
- **설명**: Your heart beats a new rhythm, as your aerial attack takes on a new manifestation. | **요구조건**: `{'equipment': 'Mantle of Enmity'}`
- **추가 정보**: Your aerial attack is replaced with Heartwing Beat, a slashing attack that applies bleed and deals Wither damage. This attack has a base damage of 25.5, copying the scaling stat from your equipped weapon. You cannot proc Air Counter or Relentless Hunt on Heartwing Beat. 6 second cooldown.

### Herbivore `[Equipment]`
- **설명**: You gain more nutrition from eating plants. | **요구조건**: `{'or': [{'equipment': "Herbalist's Hat"}, {'equipment': "Big Herbalist's Hat"}]}`

### I'm Blue `[Equipment]`
- **설명**: Improve the efficiency of your Blue Gems. Blue are the gems you use. | **요구조건**: `{'equipment': 'Bluestone Boots'}`
- **추가 정보**: Increases the effectiveness of Blue Gems by 40% additively.

### Immortality `[Equipment]`
- **설명**: The remnants of the helmet's Mind Veil stir into life when you would be made Unconscious soaking all damage for a brief duration. 30s CD. Viscosity is rejected. | **요구조건**: `{'equipment': 'Immortal Helm'}`
- **추가 정보**: Grants one instance of knock prevention. Having this Talent disables the Viscosity Enchantment.

### Inky Pearls `[Equipment]`
- **설명**: The ether you eject is coated with inky shadow. Your vent now steals a small amount of ether. | **요구조건**: `{'equipment': 'Dark Pearls'}`
- **추가 정보**: Turns your Vent black and makes it drain 47.5 Ether on hit. Additionally, your Vent can now proc certain Shadowcast Talents on hit like Sightless Still or Twisted Puppets' Shadowcast burn.

### Instant Nucleation `[Equipment]`
- **설명**: Take less damage for a few seconds after you are guardbroken. | **요구조건**: `{'equipment': 'Frost Crystal Earrings'}`

### Jester's Ruse `[Equipment]`
- **설명**: Anytime you take damage, there's a 10% chance it gets completely nullified. Anytime you deal damage, there's a 10% chance it also gets completely nullified. | **요구조건**: `{'equipment': "Jester's Beret"}`
- **추가 정보**: Visionshaper's Cheap Trick visual effect plays on proc. This can proc if an attack is blocked, dodged, or parried. When this happens, the visual effect will play, but nothing will happen.

### Laminated Armor `[Equipment]`
- **설명**: Reduces all incoming damage by 2/3 (applied after damage multipliers). | **요구조건**: `{'equipment': 'Ossified Black Pauldrons'}`
- **추가 정보**: Reduces damage taken and dealt by a flat 2 (3 in Vow of Iron). This is applied after regular resistances, allowing you to potentially fully nullify damage taken.

### Mass Effect `[Equipment]`
- **설명**: For every Might Gem you have equipped on your mantras, slightly increase each Might Gem's power. | **요구조건**: `{'equipment': 'Ascended Outlaw Hat'}`
- **추가 정보**: Increases the posture damage bonus of Might Gems by 2.25% additively, for every Might Gem you have equipped on your Mantras.

### Mindspark `[Equipment]`
- **설명**: The damage of your flames scale with how insane you are. | **요구조건**: `{'equipment': 'Necrotic Demon Horns'}`
- **추가 정보**: Your burn damage is increased based on how low your Sanity is.

### No Interruptions `[Equipment]`
- **설명**: When combat tagged by 2 or more players, render any ranged attack a lot less effective. | **요구조건**: `{'equipment': "Champion's Cape"}`
- **추가 정보**: Grants extremely high damage reduction and true hyperarmor against attacks that are coming from opponents from far away. This requires you to be combat tagged by at least two people. Self-combat tags do not count, but NPC combat tags do (you will still need to be combat tagged by at least one player for this to activate).

### No Limits `[Equipment]`
- **설명**: Increase the cap on Bloodless Gem healing. | **요구조건**: `{'equipment': "The No-Life King's Crown"}`
- **추가 정보**: Increases the cap for Bloodless Gem healing to 30. Due to Blood Necrosis reducing the healing gained from Bloodless Gems, you will need a scaled damage value of 150 to hit the 30 healing cap.

### Osseous Surge `[Equipment]`
- **설명**: Flourishing an enemy enhances your boots for 10 seconds, allowing you to spawn a wave of bones in the way you're facing. Right click to activate this. | **요구조건**: `{'equipment': 'Marrowmade Boots'}`
- **추가 정보**: Press right click within a 10 second window after landing a flourish to stomp and send a wave of bones in the direction you're facing. This deals high damage and sends your opponent upwards.

### Praise The Sun `[Equipment]`
- **설명**: When standing in sunlight increase your natural health regen and reduce how long antiheal effects last on you. | **요구조건**: `{'equipment': 'Revitalizing Pendant'}`

### Repeated Blows `[Equipment]`
- **설명**: Any strength mantra that has a Wrath Gem on it will reset its cooldown if you land a critical while a Wrath Gem is active. | **요구조건**: `{'equipment': 'Reinforced War Boots'}`
- **추가 정보**: This has no cooldown, theoretically allowing you to infinitely reset the cooldown of your Strength Mantras.

### Rock Blaster `[Equipment]`
- **설명**: Doubles your ore yields when mining. | **요구조건**: `{'equipment': "Miner's Hardhat"}`

### Seamaster's Guile `[Equipment]`
- **설명**: While you're at the helm of a ship, it takes 25% less damage | **요구조건**: `{'equipment': "Seamaster's Cap"}`
- **추가 정보**: Your boat will take 25% less damage if the person piloting it has this Talent.

### Sharpened Dagger `[Equipment]`
- **설명**: All backstabs deal 1 extra true damage (4 extra damage if done to PvE). | **요구조건**: `{'equipment': 'Ossified Blood Earrings'}`
- **추가 정보**: This applies to attacks used against your opponent's back, not assassinations.

### Simmerbloom `[Equipment]`
- **설명**: Basic Attacks on Pleeksty's Inferno are now granted flames. | **요구조건**: `{'equipment': 'Simmerbloom Diadem'}`
- **추가 정보**: Basic attacks with Pleeksty's Inferno now apply burn with no cooldown.

### Simple Buff `[Equipment]`
- **설명**: Your light attacks deal 7.5/15% more damage. Pretty simple. | **요구조건**: `{'equipment': 'Ossified Simple Pauldrons'}`
- **추가 정보**: Grants a 7.5% (15% in Vow of Iron) damage buff to M1s.

### Skillful Recovery `[Equipment]`
- **설명**: Increases passive Posture regeneration by 20% (or 35% in Vow of Iron). Recover 20% more posture when parrying attacks. | **요구조건**: `{'equipment': "Shiva's Pendant Earrings"}`

### Sloped Plate `[Equipment]`
- **설명**: Reduces the amount of damage you take when guardbroken by 10. | **요구조건**: `{'equipment': 'Ossified Black Helm'}`

### Smoldering Touch `[Equipment]`
- **설명**: Guardbreaking your opponent sets them on fire. | **요구조건**: `{'equipment': 'Ember Scorch Earrings'}`

### Sorcerer's Skill `[Equipment]`
- **설명**: Decrease the amount of tempo it takes to vent by 5. | **요구조건**: `{'equipment': 'Ether Refined Brim'}`
- **추가 정보**: This restores 5 Tempo after using your Vent instead of decreasing the Vent cost.

### Sorcerer's Surge `[Equipment]`
- **설명**: Your vent's cooldown is reduced by 2.5 seconds. | **요구조건**: `{'equipment': 'Ether Refined Mantle'}`

### Star Duster `[Equipment]`
- **설명**: You take 30% less damage from airborne enemies. | **요구조건**: `{'equipment': 'Star Duster'}`

### Stormcall `[Equipment]`
- **설명**: Anytime you land a storm strike apply stormcall shock on your opponent, damaging them if they try to use a mantra while its active. | **요구조건**: `{'equipment': 'Specialist Plate'}`
- **추가 정보**: Your Stormcall Shocks from other Specialist Equipment Talents apply the Stormcall Shock status effect. If your opponent attempts to cast a Mantra while affected, they will take 15 Galebreathe/Thundercall damage and they will gain the Shock and Winded status effect.

### Stronger Under Pressure `[Equipment]`
- **설명**: Your mantras with might gem now slow down your opponents, scaling with how many combat tags you currently have. | **요구조건**: `{'equipment': 'Ascended Outlaw Breeches'}`
- **추가 정보**: This applies an 8% slow per combat tag you have, lasting 1 second.

### Surestep `[Equipment]`
- **설명**: Your boots secure your footing in all forms of terrain by digging into the ground with metal spikes. | **요구조건**: `{'equipment': 'Delver Boots'}`
- **추가 정보**: Makes you immune to the ragdoll and movement speed debuff of the Wind from the Second Layer and Moon's Eyrie.

### Survivalist `[Equipment]`
- **설명**: Resist the effects of Weather Effects. | **요구조건**: `{'or': [{'outfit': 'Pathfinder Cloak'}, {'equipment': "Ranger's Boots"}]}`
- **추가 정보**: Take less damage from Acid Rain.

### Temple Guard `[Equipment]`
- **설명**: For the first 0.3s of your Critical Attack's windup, you take 90% less damage from any attacks that cancel your windup. | **요구조건**: `{'equipment': 'Monastery Champion Robes'}`
- **추가 정보**: You will only gain the damage reduction if your critical attack gets interrupted.

### Umami `[Equipment]`
- **설명**: Feast on foes with mighty cutlery. Chef Weapons now steal opponents hunger. | **요구조건**: `{'equipment': "Chef's Toque"}`
- **추가 정보**: Has a 35% chance to proc with a 3 cooldown per proc attempt, going on cooldown even if it fails to proc. The hunger and thirst steal are NOT affected by damage modifiers or resistances, rather exclusively being based on scaled damage dealt. Procs on: The Long Tong of The Law, The Flippers of Fate, The Pastry Paster, and Fondant Splitter.

### Volt Draft `[Equipment]`
- **설명**: Using Inhale will now also make your Basic Attacks apply a storm strike. [20 second CD] | **요구조건**: `{'equipment': 'Specialist Helmet'}`
- **추가 정보**: This has a proc window of 5 seconds after using Inhale. Storm Strikes from this Talent deal 0.125 * (Thundercall + Galebreathe investment) Thundercall damage, capping at 25 damage with 100 points invested in both Attunements. Can proc Grounding Bolt.

### Volt Reflex `[Equipment]`
- **설명**: Your dodge window is increased with the power of lightning, but also increase the cooldown of your dodges. | **요구조건**: `{'equipment': 'Authority Voltspark Mask'}`
- **추가 정보**: Increases the dodge window based on your Thundercall investment. Increases your dodge cooldown (for both dodge types) to 2.4 seconds.

### Way of the Wind `[Equipment]`
- **설명**: Being in the air briefly increases the speed of your mantra casts. This effect only lasts while you're in the air. | **요구조건**: `{'equipment': 'Gale Enhanced Earrings'}`
- **추가 정보**: On proc, a wind of gale will erupt from your legs, signifying that the effect is active.

### Whistleguard `[Equipment]`
- **설명**: The favor of the winds is yours: landing three hits (five for light weapons) without taking damage against your opponent envelops you in a shield of wind. | **요구조건**: `{'equipment': 'Whistling Periapt'}`
- **추가 정보**: The wind shield grants one (1) autoparry frame and has a cooldown of 10 seconds. The shield will be dispelled early if you get hit (proccing the shield), cast a Mantra, feint an attack, or use a critical attack.

### Winter's Protection `[Equipment]`
- **설명**: Your tightly-bound winter gear negates elemental damage buffs from weather on damage against you. Also seems to provide some resistance to the Gale. | **요구조건**: `{'equipment': 'Winter Corps Parka'}`
- **추가 정보**: Increases the time it takes for the Second Layer's parasites to kill you. Negates weather-reliant damage buffs such as Frostdraw's increased damage when its snowing or Thundercall's increased damage when it's raining.

### Woodland Terrain `[Equipment]`
- **설명**: You move slightly faster on grass. | **요구조건**: `{'equipment': 'Woodland Boots'}`

### Wormwarder `[Equipment]`
- **설명**: Your lantern generates a shroud of static electricity around you that the flesh-burrowing parasites of the Eternal Gale detest. It's not exactly the lightest thing to lug around, though. | **요구조건**: `{'equipment': 'Wormwarder Lantern'}`
- **추가 정보**: Makes you entirely immune to the Second Layer's Parasites, but at a cost of granting you a mobility debuff.

### Bane `[Outfit]`
- **설명**: Activate to make your light attacks teleport to the closest enemy nearby. | **요구조건**: `{'outfit': "Familiar Assassin's Armor"}`
- **추가 정보**: Grants a Talent tool that on use allows you to teleport to your opponent when you M1 for 20 seconds. This tool has a 100 second cooldown. The teleportation has a range limit of 25 studs. Additionally grants a speed boost for the full duration.

### Battle-Hardened `[Outfit]`
- **설명**: Reduce how much damage you take from mantra guardbreaks by 20%. | **요구조건**: `{'outfit': 'Shock Corps Light'}`

### Benefactor `[Outfit]`
- **설명**: Gain reputation for selling goods to Antiquarians within faction territories. | **요구조건**: `{'outfit': 'Varicosan Finery'}`
- **추가 정보**: Grants faction reputation upon selling items to their respective Antiquarian.

### Breeze `[Outfit]`
- **설명**: Gain a permanent +2 speed at all times. | **요구조건**: `{'outfit': "Stratos' Outfit"}`
- **추가 정보**: Increases your studs/s movement speed by +2 permanently. This is not counted as a speed buff.

### Brunt `[Outfit]`
- **설명**: While 2-handing, you take less posture damage. | **요구조건**: `{'outfit': 'Hive Tactician Armor'}`
- **추가 정보**: Reduce posture damage taken by 10% while 2 handing a weapon.

### Centurion's Resolve `[Outfit]`
- **설명**: Your Legion Kata/Imperium Kata attacks deal 4% more damage. | **요구조건**: `{'outfit': 'Legion Centurion'}`

### Chief's Will `[Outfit]`
- **설명**: Way of Navae light attacks have 10% additional penetration. | **요구조건**: `{'outfit': 'Navaen War Chief'}`
- **추가 정보**: Gives M1 attacks and criticals with the M1 tag +10% PEN if you are using the Way of Navae fist style.

### Circuit Breaker `[Outfit]`
- **설명**: Electrify no longer deals self-damage on use. | **요구조건**: `{'outfit': "Stormchanter's Raiments"}`
- **추가 정보**: Using this with the Deepscorn Casque will cause you to heal upon using Electrify.

### Corrosive Touch `[Outfit]`
- **설명**: Landing a successful Critical Attack or Flourish will corrode a portion of your opponent's Armor. | **요구조건**: `{'outfit': "Arachnid's Weave"}`
- **추가 정보**: On proc, drain 5% of your opponent's armor. This has a 10 second cooldown.

### Crippling Darkness `[Outfit]`
- **설명**: Your non-Basic Attacks have 20% PEN. | **요구조건**: `{'outfit': "Prophet's Cloak"}`
- **추가 정보**: Grants +20% PEN to any non-weapon attack. This not only affects Mantras, but things like Bleed or Burn too.

### Demon Step `[Outfit]`
- **설명**: Activate to gain brief iframes while moving forward. This requires 50 ether to activate and increases your posture by 20% each use. | **요구조건**: `{'outfit': "Familiar Demon's Armor"}`
- **추가 정보**: On use, lose 50 Ether to travel a short distance forwards in iframes. Additionally, 20% of your current posture will be dealt to you as self-posture damage.

### Devastating Power `[Outfit]`
- **설명**: Gain extra Ether for every Mantra in your arsenal. | **요구조건**: `{'outfit': 'Pathfinder Arch-Sorcerer'}`
- **추가 정보**: Gain 10 maximum Ether for every Mantra you have equipped.

### Ferryman's Curse `[Outfit]`
- **설명**: Wearing this gives you a 20% chance to convert incoming elemental damage into Lightning damage. | **요구조건**: `{'outfit': "Ferryman's Coat"}`

### Fists of Navae `[Outfit]`
- **설명**: Double the amount of ether you gain on successful light attacks. | **요구조건**: `{'outfit': 'Navaen Nomad Robes'}`

### Fleetfoot `[Outfit]`
- **설명**: Gain an initial speed boost when slide jumping. | **요구조건**: `{'outfit': 'Carefree Garments'}`
- **추가 정보**: After using a Lightning or Gale dash, all dashes within the next 3 seconds will become enhanced. These enhanced dashes have the same effectiveness as Lightning and Gale dashes.

### Focused Hematoma `[Outfit]`
- **설명**: Increase the amount of temporary health you receive by 15%. | **요구조건**: `{'outfit': 'Sanguine Finery'}`

### Hunter's Reflexes `[Outfit]`
- **설명**: You have a slightly larger dodge window. | **요구조건**: `{'outfit': 'Cutthroat Light Armor'}`
- **추가 정보**: Increases the dodge window by 0.05s.

### Hyperbody `[Outfit]`
- **설명**: Apply a buff to your allies around you that increases your speed, defense, and regeneration. This effect becomes weaker the more allies you buff with it. | **요구조건**: `{'outfit': "Familiar Knight's Armor"}`
- **추가 정보**: Provides 35.5% damage reduction, scaling up with the amount of players buffed. Provides a 7.5 studs/s movement speed bonus, scaling down with the amount of players buffed. Hyperbody has a 30 second duration, but this duration will be reduced by 3s for every player buffed (including yourself). 2 minute cooldown.

### Intrepid Flame `[Outfit]`
- **설명**: Flames wear off twice as fast on you. Flames that come from your Flame Within deal much less damage on you. | **요구조건**: `{'outfit': 'Flame Worshipper Armor'}`
- **추가 정보**: Halves the maximum burn duration.

### Knack `[Outfit]`
- **설명**: Trees yield more Wood when felled. Your Repair speed is increased. | **요구조건**: `{'outfit': 'Eager Tradesman'}`

### Legendary `[Outfit]`
- **설명**: Parrying and landing hits with your weapon gives you ether back. | **요구조건**: `{'outfit': 'Grand Pathfinder Cloak'}`

### Lethal Dose `[Outfit]`
- **설명**: The poison from your hidden blade lasts twice as long. | **요구조건**: `{'outfit': 'Inquisition Light'}`
- **추가 정보**: Doubles the duration of the Hidden Blade poison effect, from 8 seconds to 16.

### Life Leech `[Outfit]`
- **설명**: Your summons now heal you each time they deal damage. | **요구조건**: `{'outfit': "Familiar Occultist's Armor"}`
- **추가 정보**: The healing gained is based on summon damage dealt. This works on the following summons: monsters from the Parasol's Blight enchantment, The Weaving Web's critical attack, Illusory Servants, Illusory Counter, Lightning Clones, and Flame Sentinel.

### Looter `[Outfit]`
- **설명**: Get extra loot from items you turn in for rewards. | **요구조건**: `{'outfit': 'Experienced Adventurer'}`
- **추가 정보**: This affects: turning in Artifacts or the Strange Egg at a banker, turning in Sacks to Mercille, handing in pure ore to a Blacksmith, and trading in Explosive Crates to Scope.

### Merchant's Accord `[Outfit]`
- **설명**: Merchants and Antiquarians will do business with you no matter how poor your reputation is. | **요구조건**: `{'outfit': 'Merchant Robes'}`
- **추가 정보**: This Talent does NOT allow you to use the Antiquarian in the First Layer if you are not Deepbound or Ignition Delver.

### Mocking Favor `[Outfit]`
- **설명**: When taunting, Aelita or Tillian appears, bestowing upon you a random boon of affliction. (30s cooldown) | **요구조건**: `{'or': [{'outfit': "Jester's Grab"}, {'outfit': "Trickster's Habit"}]}`
- **추가 정보**: Grants a random buff or affliction from a set list whenever you spit or use an emote.

### Overwhelming Might `[Outfit]`
- **설명**: Strong Left now guard breaks at level 5. | **요구조건**: `{'outfit': "Titus's Raiment"}`
- **추가 정보**: 60 second cooldown.

### Paired Soul `[Outfit]`
- **설명**: Wielding a katana with this outfit grants extra damage. | **요구조건**: `{'or': [{'outfit': 'Vigil Initiate'}, {'outfit': 'Cloak of Winds'}, {'outfit': 'Royal Etrean Guard'}]}`
- **추가 정보**: Katana deals 25% more damage. Alloyed Katana, Shattered Katana, and Purple Cloud deal 5% more damage. This is a damage modifier.

### Primal Rage `[Outfit]`
- **설명**: If you are below 50%, unleash your rage and increase the amount of damage you deal for 25 seconds as well as being able to see enemy health when you hit them. | **요구조건**: `{'outfit': "Titanslayer's Adornment"}`
- **추가 정보**: Grants a Talent tool that can only be used when you are under 50% health. While buffed, your hits will showcase the health percentage of your opponent. Additionally, gain a 25% damage buff for the duration of the effect. 3 minute cooldown.

### Refreeze `[Outfit]`
- **설명**: Landing any sort of ability that causes bottom freeze reduces the cooldown of your Orbital Ice by 20 seconds. | **요구조건**: `{'outfit': "Icebringer's Vestments"}`

### Repeated Propulsion `[Outfit]`
- **설명**: Reduce the cooldown of Dancing Steps and Graceful Steps to 1 second. | **요구조건**: `{'outfit': 'Cindergarb'}`

### Riot Breaker `[Outfit]`
- **설명**: You receive 15% less posture damage and deal 10% more posture damage when under attack by 3 or more enemies. | **요구조건**: `{'outfit': 'Authority Commander'}`

### Scholar's Intuition `[Outfit]`
- **설명**: INT, WILL, and CHA Training Gear is 50% more effective. | **요구조건**: `{'outfit': 'Scholar'}`

### Serpent's Dance `[Outfit]`
- **설명**: Unleash the power of Fang and Coil to unlock a devastating Running Critical Attack, feint to cancel momentum. | **요구조건**: `{'outfit': "Jade Vigil's Weave"}`
- **추가 정보**: This critical deals 1x of your weapon's scaled damage. This critical can only be used on Cestus that do not have a unique critical.

### Soul Rip `[Outfit]`
- **설명**: Kill a player to gain 2 runes. Activate a rune when using this talent, and gain immense physical power, defense, and infinite ether for 25 seconds. Beware its strenuous downside. | **요구조건**: `{'outfit': "Familiar Heretic's Armor"}`
- **추가 정보**: Grants a 50% weapon damage buff, ?% defense, infinite Ether, and a speed boost for the buff duration. Once the buff wears off, one of your legs will break, removing your ability to sprint for 30 seconds.

### Sunset Ricochet `[Outfit]`
- **설명**: Makes your bullets ricochet to a nearby enemy when hitting an opponent. | **요구조건**: `{'outfit': 'Summer Dragoon'}`

### Tempest Evolution `[Outfit]`
- **설명**: Your slide-jumped Wind Blades are naturally stronger and if landed grant +20% damage in the air for a few seconds. | **요구조건**: `{'outfit': "Tempestmaker's Threads"}`
- **추가 정보**: Increases the slide jump variant of Wind Blade's damage by 20%. Additionally grants a 20% damage buff for 15 second after landing slide cast Wind Blade. This damage buff only applies while you are airborne.

### The Path, Unveiled `[Outfit]`
- **설명**: Your Jus Karita attacks deal 10% more damage. | **요구조건**: `{'or': [{'outfit': 'Justicar'}, {'outfit': 'Mod Suit'}]}`

### Tidekeeper `[Outfit]`
- **설명**: Losing 25% of your health within the span of 3 seconds grants a 15% damage buff, 20% defense buff, and prevents from being knocked for 10 seconds. | **요구조건**: `{'outfit': 'Celtorian Tideknight'}`

### Tidal Shock `[Outfit]`
- **설명**: Landing a successful Critical Attack will temporarily put you in a state where you dodge all mantras, as well as dazing your opponent. | **요구조건**: `{'outfit': 'Cala-Mariner'}`
- **추가 정보**: Your Critical attacks will apply Daze on hit. For the next 4 seconds after landing your Critical attack, if you were to be hit by any Mantra, you'll automatically dodge the Mantra instead, voiding its damage. This can be used to void self damaging Mantras. 13 second cooldown.

### Unbreakable `[Outfit]`
- **설명**: You have reduced stun duration when block broken. | **요구조건**: `{'or': [{'outfit': 'Darksteel Plate'}, {'outfit': 'Etrean Guard'}]}`
- **추가 정보**: Reduces the stun duration from being guardbroken by 33%; from 1.05s to 0.7s.

### Vigil's Grace `[Outfit]`
- **설명**: Whenever you gain a speed boost, increase your swingspeed by 0.02. | **요구조건**: `{'outfit': 'Vigil Sentinel'}`
- **추가 정보**: Stacks additively with Action Surge. Both this and Action Surge are applied before Lightning Cloak's swing speed multiplier.

### Wind Dancer `[Outfit]`
- **설명**: Roll cancelling twice in quick succession will grant you a speed boost. One of your rolls must dodge a hit. | **요구조건**: `{'outfit': 'Windrunner Robes'}`
- **추가 정보**: Grants a 10% speed boost for 8 seconds. 10 second cooldown.

### Withering Soul `[Outfit]`
- **설명**: Your Basic Attacks proc 12.5% of their damage as Wither. Wielding the Deepspindle or Umbrite Witherblade will double the amount to 25%. | **요구조건**: `{'outfit': 'Darkened Bastion'}`
- **추가 정보**: The Wither applied is based off your weapon's scaled damage.

### Bloodless Overdrive `[Equipment]`
- **설명**: Gain bonus temp health everytime you land a mantra with a Bloodless Gem. | **요구조건**: `{'set': 'Bloodcurdle'}`

### Captain's Call `[Equipment]`
- **설명**: Call up two Blacksteel Pirates to aid you in battle. | **요구조건**: `{'set': 'Ossified Black'}`
- **추가 정보**: On use, this summons two allied Blacksteel Pirates to assist you. 5 minute cooldown.

### Critical Heal `[Equipment]`
- **설명**: Every time you heal, you have a chance to proc a Critical Heal, healing you 30 health. [5 second CD] | **요구조건**: `{'set': 'Regenerative'}`

### Enforcer's Pull `[Equipment]`
- **설명**: Your Enforcer's Pull is improved. Land a flourish to make it even stronger. | **요구조건**: `{'set': 'Hardened Enforcer'}`

### Etherguard `[Equipment]`
- **설명**: Warped Blue Gems now provide a bonus effect when landed using a mantra, Etherguard. This effect gives extra resistances to mantras based on how much ether they cost to cast + gain elemental protection against PvE. | **요구조건**: `{'set': 'Bluestone'}`
- **추가 정보**: When landing a Mantra with a Warped Blue Gem equipped, gain the Etherguard status effect, granting you damage reduction to Mantras and elemental resistance in PvE. The damage reduction for Mantras scales on the Ether cost of the Mantra you got hit by.

### Lasting Trauma `[Equipment]`
- **설명**: Anytime you land a Wrath Gem, your opponent becomes fearful, being unable to use their critical for a few seconds after you land it. This also buffs Fatal Strike, causing it to deal 15 true damage on proc. | **요구조건**: `{'set': 'Reinforced War'}`
- **추가 정보**: This applies the Fearful status effect for 19 seconds. Wrath gems have a 10 second cooldown, meaning you can potentially disable your opponent's ability to use their critical indefinitely. You deal 15 true damage if you guardbreak an opponent with a Strength Mantra that has a Wrath Gem on it.

### Offensive Recovery `[Equipment]`
- **설명**: If all your mantras have Might Gems equipped, lose posture any time you hit opponents block with a mantra. | **요구조건**: `{'set': 'Ascended Outlaw'}`
- **추가 정보**: If all of your equipped Mantras have a Might Gem equipped, hitting your opponent's block with Mantras will restore your posture.

### Shock Trooper Specialist `[Equipment]`
- **설명**: Empower the mantras taught to you by your Legion Specialist Captain. You also now conjure a storm strike on your opponent by landing Gale and Thundercall mantras. | **요구조건**: `{'set': 'Specialist'}`
- **추가 정보**: Upon meeting a damage threshold, create a Stormcall Strike. The Storm Strikes deal 40 Thundercall damage and can proc Grounding Bolt. Additionally, your Electro Carve, Grand Javelin, and Thunder Kick become green, and your Astral Wind, Champion's Whirlthrow, and Gale Lunge become yellow. All of the aforementioned Mantras have their base damage increased by 15%.

### Sorcerer's Supply `[Equipment]`
- **설명**: Increase the amount of Tempo you have by 10/30. | **요구조건**: `{'set': 'Ether Refined'}`
- **추가 정보**: Increases your Tempo by 10 in Pathfinder or 30 in Vow of Iron.

### Test `[Spec]`
- **설명**: 설명 없음 | **요구조건**: `{'outfit': 'Etrean Rogue'}`
- **추가 정보**: This is a placeholder Talent for a placeholder Outfit.

### Residual Fury `[Memento]`
- **설명**: [In Berserk State] Landing your critical grants +50% PEN on Basic Attacks for 8s. | **요구조건**: `{'stats': {'Power': 10}, 'objectives': ['Purchase in Shop'], 'memento': 'Berserker'}`

### Righteous Rage `[Memento]`
- **설명**: [In Berserk State] You deal increased damage the lower your health is. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Berserker'}`
- **추가 정보**: Temporary Health does not count for this effect.

### Rip and Tear `[Memento]`
- **설명**: Regain health upon defeating an enemy. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Berserker'}`

### Ruinous Recovery `[Memento]`
- **설명**: Enemies recover 15% less Posture when parrying. Guardbreaking an enemy by parrying them deals massive damage, and can be done against even the strongest of foes. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Berserker'}`

### Until It Is Done `[Memento]`
- **설명**: Your Berserk State lasts until you willingly end it. | **요구조건**: `{'memento': 'Berserker'}`
- **추가 정보**: Your Berserk has an indefinite duration, ending only when you use the tool again.

### Breakthrough `[Memento]`
- **설명**: Posture damage on light attacks are increased by 10%. | **요구조건**: `{'stats': {'Power': 5}, 'objectives': ['Purchase in Shop'], 'memento': 'Breaker'}`
- **추가 정보**: Increases the posture damage of M1s by 10%.

### Calamity Punch `[Memento]`
- **설명**: Every successful Strong Left builds up stacks to perform a larger scale punch. | **요구조건**: `{'memento': 'Breaker'}`

### Dormant Strength `[Memento]`
- **설명**: At max Calamity Punch stacks increased posture damage & physical damage. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Breaker'}`
- **추가 정보**: Increases your Strong Left's damage and posture damage if you are at max Calamity Punch stacks.

### Relentless Barrage `[Memento]`
- **설명**: Every swing from Rapid Punches deals more posture than the last. At max punch stacks enables hyperarmor during the barrage. | **요구조건**: `{'stats': {'Power': 15}, 'objectives': ['Purchase in Shop'], 'memento': 'Breaker'}`
- **추가 정보**: Your Rapid Punches posture damage per hit scales on the amount of hits landed/blocked. At max Calamity Punch stacks, gain hyperarmor during Rapid Punches.

### Shattering Left `[Memento]`
- **설명**: Your Strong Left and Wind-up punches will always guard break mobs. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Breaker'}`
- **추가 정보**: Turns your Strong Left and Wind-Up enhanced attacks into guaranteed guardbreaks against blocking NPCs.

### Threefold Impact `[Memento]`
- **설명**: Every stack built with Strong Left provides a buff. 1st successful attack will reduces cooldown, 2nd ignores armor, and 3rd increases damage & guardbreaks. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Breaker'}`
- **추가 정보**: Grants buffs to your Strong Left based on how many Calamity Punch stacks you have. At one stack, your Strong Left cooldown will be reduced. At two stacks, your Strong Left will additionally deal typeless damage. At three stacks, your Strong Left will also guard break and deal more damage.

### Blessing of the Moonseye `[Memento]`
- **설명**: The Moonseye is not one eye, but many. All of them watch you. All of them know of your sins. | **요구조건**: `{'objectives': ["Go to the Moon's Eyrie and interact with the beam of light."]}`
- **추가 정보**: Upon obtaining this Talent, you will lose all of your Sanity permanently. Defeating the three main progression bosses while having this Talent will unlock the Prince of the Moon Memento.

### Ether Blade `[Common]`
- **설명**: Draw your foes ether into your weapon when you parry ether-based attacks. Gain Ether when you parry mantras. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Strange Merchant'}`

### Blinkstep `[Memento]`
- **설명**: Your regular dash is enhanced into a Blinkstep above 90% ether but now has an ether cost. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Drifter'}`
- **추가 정보**: If you have 90% or more Ether, your regular dash will be replaced with a Blinkstep. This has much more distance than a regular dash. Consumes Ether on use.

### Cutting Pace `[Memento]`
- **설명**: Dodging attacks will now grant 'Cutting Pace' stacks. Mantras and basic attacks consume a stack to shorten wind-up and increase damage, procs after dash. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Drifter'}`
- **추가 정보**: Buffed attacks deal 15% more damage, have a slightly shorter windup, and are purple.

### Drift `[Memento]`
- **설명**: You're no longer slow enough to have to rely on parries. Dodge instead. | **요구조건**: `{'memento': 'Drifter'}`
- **추가 정보**: Your parry is replaced with a low distance dodge if you successfully parry an attack.

### Drifting Cloud `[Memento]`
- **설명**: Cutting Pace now unsheathes the full potential of your Purple Cloud. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Drifter'}`
- **추가 정보**: Proccing Cutting Pace now unsheathes your Purple Cloud, giving it new animations and changing the damage type to Slash.

### Faster Blade `[Memento]`
- **설명**: A successful "Drift" now grants a speed boost. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Drifter'}`
- **추가 정보**: Procs when "parrying" an attack.

### Lackluster Guard `[Memento]`
- **설명**: You aren't used to having to block, resulting in weaker posture. | **요구조건**: `{'memento': 'Drifter'}`
- **추가 정보**: Reduces your maximum posture.

### True Drifter `[Memento]`
- **설명**: You are a true drifter. Gain double the 'Cutting Pace' stacks and consume stacks to Blinkstep below 90% ether. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Drifter'}`
- **추가 정보**: Anytime you would have gained 1 Cutting Pace stack, gain 2 instead. You can now consume Cutting Pace stacks to use Blinkstep without being at 90% or more Ether.

### Twin Drift `[Memento]`
- **설명**: Hitting an enemy in the back after a roll cancel will bring upon twins who will follow up your assault. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Drifter'}`
- **추가 정보**: Performing a basic attack after a roll cancel will perform a second slash, then two light purple clones of yourself will attack the target.

### Barrage Mastery `[Memento]`
- **설명**: For every Ether Erudite stack you have, gain one extra orb whenever you fire your Ether Barrage. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Ether Erudite'}`
- **추가 정보**: Increases the projectile count of Ether Barrage based on how many stacks of Ether Erudite you have.

### Ether Amplification `[Memento]`
- **설명**: For every Ether Erudite Stack you have, increase the size and damage of your Pressure Blast. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Ether Erudite'}`
- **추가 정보**: Turns Pressure Blast light blue.

### Ether Blitz `[Memento]`
- **설명**: For every Ether Erudite Stack you have, reduce the windup of your enhanced Master's Flourish. This consumes your Ether Erudite stacks on use. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Ether Erudite'}`
- **추가 정보**: Turns Master's Flourish light blue.

### Ether Burst `[Memento]`
- **설명**: Landing Rapid Slashes on your opponent gives them an overflow of Ether, causing them to take bursts of damage based on how many Ether Erudite stacks you had. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Ether Erudite'}`
- **추가 정보**: Consumes your Ether Erudite Stacks. Turns your Rapid Slashes light blue.

### Ether Erudite `[Memento]`
- **설명**: The more total Ether you have, the more damage you deal. Gain Ether Erudite Stacks to improve your combat abilities. The max amount you can hold is 6. | **요구조건**: `{'memento': 'Ether Erudite'}`

### Ether Quell `[Memento]`
- **설명**: Landing a Critical Attack or Guardbreaking an opponent gives you 1 Ether Erudite Stack. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Ether Erudite'}`

### Ether Reflux `[Memento]`
- **설명**: Successfully countering an opponent with Prediction gives you 2 Ether Erudite stacks. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Ether Erudite'}`

### Flames of the Past `[Memento]`
- **설명**: Your flamecharm mantras now call forth fiery homing spirits. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Flame Worshipper'}`
- **추가 정보**: Your Flamecharm Mantras now spawn Twisted Puppets' Puppets on hit.

### Pleetsky's Wrath `[Common]`
- **설명**: After dealing 500 damage with Flame Mantras, call forth a hail of fiery swords. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Flame Worshipper'}`
- **추가 정보**: Spawns swords from the sky, similarly to First Light's critical attack.

### Electrical Accumulation `[Memento]`
- **설명**: While having 4 or more orbs, automatically gain 4 charges of Static Blade whilst you have 4 orbs. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Flashing Thunder'}`
- **추가 정보**: Passively gain 4 stacks of Static Blade if you have 4 or more orbs.

### Gathering Storm `[Memento]`
- **설명**: Your damage is stored in a lightning orb. Sheathing your weapon will shoot the lightning orbs at the opponent. The orbs will do more damage based on how many orbs are being stored up. | **요구조건**: `{'memento': 'Flashing Thunder'}`
- **추가 정보**: All weapon damage is stored instead of being dealt initially, similar to the Poser's Ring. Upon reaching damage thresholds of stored damage, lightning orbs will appear above your character's head, with a cap of 8 orbs. Upon sheathing your weapon, the orbs will attack your opponent, dealing all of the stored damage at once.

### Heir of Lightning `[Memento]`
- **설명**: At max orbs, Lightning Cloak is enhanced. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Flashing Thunder'}`
- **추가 정보**: Increases the base duration of Lightning Cloak to 15 seconds.

### Orb Discharge `[Memento]`
- **설명**: If an extra orb is available, you can consume it to vent if you don't have enough tempo. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Flashing Thunder'}`

### Command Phoenix `[Memento]`
- **설명**: Command your Phoenix to scout, and dive into enemies. | **요구조건**: `{'memento': 'Solborn'}`
- **추가 정보**: Summoning an adult Phoenix, then commanding it to take air will allow you to select a spot where it should Divebomb on the next usage of the Talent.

### Heliodar Wings `[Memento]`
- **설명**: Take flight [H]. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Solborn'}`
- **추가 정보**: Pressing H will sprout your Heliodar Wings. Hold Space while flying to ascend, Q to speed up, or CTRL to descend. Flying consumes Heartfire Gauge. If you run out of Heartfire Gauge while flying, you will be set on fire, ending the flight early. Taking damage from any source will cause your flight to end early.

### Ascended Phoenix Flames `[Memento]`
- **설명**: Once per fight, when an attack would down you immediately revive with 30% HP. | **요구조건**: `{'or': [{'slay': "Shogun of the Prophet's Guard", 'memento': 'Flame Worshipper'}, {'slay': 'True Heart of Enmity', 'memento': 'Solborn'}]}`

### Prince of the Wind `[Memento]`
- **설명**: You are the one who the wind bends around. Your galebreathe is enhanced. | **요구조건**: `{'memento': 'Inheritor of the Gale'}`

### Hardened Shell `[Innate]`
- **설명**: Your Natural Armor grows sturdier, being able to take more hits before breaking. | **요구조건**: `{'aspect': 'Vesperian'}`
- **추가 정보**: Increases your Natural Armor durability.

### Steady Mind `[Innate]`
- **설명**: Despite the finality of your mind and body succumbing to the effects of the depths, you manage to ward it off for a little longer. | **요구조건**: `{'aspect': 'Ganymede'}`
- **추가 정보**: You can spend more time in the Depths before gaining Afflictions.

### Glide Mastery `[Innate]`
- **설명**: Experience using the glider you crafted results in you being able to glide faster in the air. You've also trained to quickly pull it out in dire situations, resulting in you no longer taking fall damage. | **요구조건**: `{'aspect': 'Tiran'}`

### Acute Hearing `[Innate]`
- **설명**: After years of using Echolocation, you've trained your ears to sense danger from even further away. You are also able to sense when someone completes a job. | **요구조건**: `{'aspect': 'Kiron'}`
- **추가 정보**: Your Echolocation now has a sound effect on proc.

### From The Ashes `[Innate]`
- **설명**: Using an Etris Flask when at 30% health or below now grants you a damage buff and resistance buff for 30 seconds. | **요구조건**: `{'aspect': 'Heliodar'}`

### Lone Wolf `[Innate]`
- **설명**: Despite the loyalty of your allies, you recognize that you sometimes need to hunt alone. Deal more damage to targets who are only combat tagged by you. | **요구조건**: `{'aspect': 'Canor'}`

### Scales of the Edenkite `[Innate]`
- **설명**: In order to resolve conflict in Lumen, you need to be able to handle any situation thrown at you. Activate your Scales to reduce all damage taken by 80% and de-aggro enemies briefly. | **요구조건**: `{'aspect': 'Drakkard'}`
- **추가 정보**: Grants a Talent tool that lasts 5 seconds with a 3 minute cooldown. The deaggro effect only works in PvE, and is extremely ineffective, as most enemies will immediately reaggro. The deaggro effect does not work against bosses or in Depths Trials.

### Scholar's Mark `[Innate]`
- **설명**: You now are able to inflict yourself with a Mark. The duration of this scales with how many people you inflict with the effect as well. | **요구조건**: `{'aspect': 'Capra'}`
- **추가 정보**: You can now use Capra Marks to buff yourself.

### Largent `[Innate]`
- **설명**: Your diplomatic skills extend into your ability to barter. Gain 300 extra notes per chest when turning in a sack. | **요구조건**: `{'aspect': 'Adret'}`

### Tailor Made `[Innate]`
- **설명**: These were specifically made for your kind. Etris Flasks now heal you 45% more than usual. | **요구조건**: `{'aspect': 'Etrean'}`

### Mothwing Defense `[Innate]`
- **설명**: Further refining how sharp your antennae, you can now immediately recognize a sneak attack and brace yourself for it. Reduce all backhit damage by 50%. | **요구조건**: `{'aspect': 'Chrysid'}`

### Navae's Technique `[Innate]`
- **설명**: A passed down technique from generations ago to refine your Ether control. Reduce how much ether it takes to cast mantras by 30%. | **요구조건**: `{'aspect': 'Gremor'}`

### Innate Agility `[Innate]`
- **설명**: You hinge on your instincts to keep you alive, even in battle. Slightly increase your dodge frames. | **요구조건**: `{'aspect': 'Felinor'}`

### Retrograde `[Innate]`
- **설명**: Your existence is... questionable. No one understands where you have come from. Your ability reflects this, activate to start your Retrograde timer. Activating the ability again will reverse your actions, with the cooldown scaling with the time. | **요구조건**: `{'aspect': 'Levit'}`
- **추가 정보**: Gain a Talent tool that records your location, health, Ether, and posture on use. Upon using the tool again or waiting 5 seconds, you will be transferred back to your original location, restoring you back to the state and location you were at when this tool was initially used.

### Depths Denizen `[Innate]`
- **설명**: The city you once called home is now your only way out of the depths, perhaps you can use this to your advantage. Gain extra leeway when attempting to escape the depths. | **요구조건**: `{'aspect': 'Celtor'}`

### Weapon's Training `[Innate]`
- **설명**: Training with different weapons taught you how to wield all of them more proficiently. Gain slightly extra weapon scaling on all weapons you use. | **요구조건**: `{'aspect': 'Khan'}`

### Alloy of the Heavens `[Memento]`
- **설명**: Posture attack from mobs reduced by 50% | **요구조건**: `{'stats': {'Power': 10}, 'objectives': ['Purchase in Shop'], 'memento': 'Iron Vessel'}`
- **추가 정보**: Reduces posture damage taken from mobs by 50%.

### Deal Maker `[Memento]`
- **설명**: Your rapport with merchants allows you to attach a flat fee of 20 notes to all your sales. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Strange Merchant'}`
- **추가 정보**: This is unaffected by Snake Oil.

### Know When To Run `[Memento]`
- **설명**: Your magic coffin has a higher chance to draw depths loot, but the price is increased. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Strange Merchant'}`
- **추가 정보**: Increases the price of using the Magic Coffin by 50% in exchange for adding the entire Depths lootpool to it.

### Stack the Deck `[Memento]`
- **설명**: Charmed enemies will grant you even more damage multipliers on your Taunt counter. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Strange Merchant'}`

### Soul Veil `[Memento]`
- **설명**: Soulthorn now directly siphons the song of your enemies. Accumulating stacks and increasing your power. Perfect plays are encouraged. | **요구조건**: `{'memento': 'Prince of the Moon'}`
- **추가 정보**: Each successful attack with the Soulthorn builds up stacks of Soul Veil, increasing your weapon damage by 7.5%. This caps at a 30% damage buff. If you take damage while Soul Veil is active, the opponent who hit you will steal your Soul Veil stacks until you hit them back. This can prove fatal.

### Ambush `[Memento]`
- **설명**: When coming out of Tacet, gain a 30% damage boost for 5 seconds. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Rogue Assassin'}`

### Avaricious Blade `[Memento]`
- **설명**: Every strike landed lines your pockets. | **요구조건**: `{'memento': 'Rogue Assassin'}`
- **추가 정보**: Dealing damage by any means gives 1 Note, with backhits giving 50 Notes instead. This can proc on self damage.

### Double Jump `[Memento]`
- **설명**: Take the Wind Step and refine it into your own technique, reducing the cooldown and improving its efficiency. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Rogue Assassin'}`
- **추가 정보**: Reduces Wind Step's cooldown to 5 seconds and lowers the Ether cost. You will need to equip Gale Boots to gain the Wind Step Talent.

### Fatal Backstab `[Memento]`
- **설명**: Weapon backstabs deal an extra 5 true damage on your opponent (20 extra damage if done to PvE). | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Rogue Assassin'}`

### Lethal Depressant `[Memento]`
- **설명**: Assassinating an opponent decreases the damage they deal by 25% for the next 30 seconds. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Rogue Assassin'}`

### Rogue Assassin `[Memento]`
- **설명**: Your assassinations now deal an extra 50 true damage (200 in PvE). | **요구조건**: `{'memento': 'Rogue Assassin'}`

### Terrifying Paralysis `[Memento]`
- **설명**: Your Hidden Blade disables opponents' ability to roll for 3 seconds. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Rogue Assassin'}`

### Total Silence `[Memento]`
- **설명**: Massively reduce the sound of your footsteps and rolls. | **요구조건**: `{'stats': {'Power': 20}, 'objectives': ['Purchase in Shop'], 'memento': 'Rogue Assassin'}`

### True Skulk `[Memento]`
- **설명**: Massively reduce the sounds of your mantra casts. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Rogue Assassin'}`

### Weakening Venom `[Memento]`
- **설명**: Assassinating an opponent decreases the damage they deal by 25% for the next 30 seconds. | **요구조건**: `{'memento': 'Rogue Assassin'}`

### Frostride `[Memento]`
- **설명**: Your footsteps echo the legend of Saint Jay, freezing the sea beneath. | **요구조건**: `{'stats': {'Power': 10}, 'objectives': ['Purchase in Shop'], 'memento': 'Saint Jay'}`
- **추가 정보**: You can now walk on water by creating ice below your feet. This has no cooldown and does not cost Ether.

### Jay's Judgement Gavel `[Memento]`
- **설명**: Breaking a frozen enemy free with your Critical saps their lifeforce. | **요구조건**: `{'memento': 'Saint Jay'}`
- **추가 정보**: Landing your critical on a frozen or bottom frozen enemy will deal extra damage and heal you.

### Rebuke in Stasis `[Memento]`
- **설명**: Bottom freeze enemies nearby when countering with Punishment, freezes mobs affected when re-casted. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Saint Jay'}`
- **추가 정보**: Your Punishment will apply bottom freeze to mobs if you land the counter hit.

### Verses of Harmony `[Memento]`
- **설명**: Each elemental stance grants access to select talents from the corresponding attunement. | **요구조건**: `{'memento': 'Saintsworn'}`
- **추가 정보**: Gain access to the following Talents while in the respective Saint Stance. Upon swapping out of the Saint Stance, all granted Talents will be lost. Some of these Talents have an additional level requirement.
Flamecharm: Dancing Steps, Immolation, Agitating Spark
Frostdraw: Condensation Drip, Saint Jay, Frozen Legs, Fragile Freeze, Chilling Flourish
Galebreathe: Pressure Break, Wind Step, Air Pressure, Cyclone Blade, Inhale, A World Without Song
Shadowcast: Dark Rift, Lasting Sorrow, Dark God, Dark Hours, Shadow Overflow, Singularity
Thundercall: Static Fakeout, Stratoshock, Resolve Crusher, Static Blade, Gathering Electricity

### Focused Perception `[Memento]`
- **설명**: Massively increase the range of your Rhythm if you use it while Tranquil Circle is active. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Sightless'}`

### Purge Shot `[Memento]`
- **설명**: Landing an arc beam while your opponent has anti heal stacks purges the stacks, with it dealing 5 true damage for every stack they had. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Sightless'}`
- **추가 정보**: Landing Arc Beam removes all stacks of anti-heal from your opponent, dealing 5 true damage for every stack they had.

### Scornful Scowl `[Memento]`
- **설명**: Your Glare stuns enemies for much longer. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Sightless'}`

### Unmended Eye `[Memento]`
- **설명**: All mantras you land now apply anti heal. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Sightless'}`

### Dancer's Beat `[Memento]`
- **설명**: Your Vent is replaced with Dancer's Beat. You increase the speed, damage, and stun of your next Basic Attack. However, should your attack fail to land, you'll be stunned and your Tempo will be greatly reduced. | **요구조건**: `{'memento': 'Spear Dancer'}`
- **추가 정보**: Your Vent can no longer be used defensively, unless it is used to escape an otherwise inescapable move, but does not cost Tempo to use. You need to have at least 20 Tempo to use Dancer's Beat. Your next M1 used within 1 second of using Dancer's Beat will deal higher damage, more stun, and have a higher swing speed. If you are hit before you use your next attack, wait out the 1 second proc window, or if your next attack does not land (including if it was blocked, parried, or dodged), you will lose 60 Tempo and will be stunned for 0.5 seconds. 2.5 second cooldown.

### Dancer's Geas `[Memento]`
- **설명**: You deal +30% damage when striking with the tip of your weapon, but deal 15% less damage when striking below half of its range. | **요구조건**: `{'memento': 'Spear Dancer'}`
- **추가 정보**: Also procs on weapon criticals. When you land an attack from the tip of your weapon, an icon of a pair of hands clapping will appear, signifying that you've activated the buff. When you land an attack from half or less than half of your weapon's range, an icon of a thumbs down will appear, signifying that you were debuffed.

### Dancer's Impale `[Memento]`
- **설명**: Hitting an enemy after a perfect dodge makes your next attack deal 30% bleed damage. If that attack would already bleed, it adds +10% chip damage instead. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Spear Dancer'}`

### Dancer's Sting `[Memento]`
- **설명**: Striking with the tip of your weapon applies +25% PEN and +25% Chip Damage. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Spear Dancer'}`

### Ga Buidhe `[Memento]`
- **설명**: Backstabs now count as the tip of your weapon. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Spear Dancer'}`
- **추가 정보**: Attacking your opponent's back now procs all Talents and effects that would normally proc when attacking with the tip of your weapon.

### Ga Dearg `[Memento]`
- **설명**: Striking a bleeding enemy with the tip of your weapon extends the bleed. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Spear Dancer'}`
- **추가 정보**: Hitting a bleeding enemy with the tip of your weapon will reapply the bleed.

### Kick the Beat `[Memento]`
- **설명**: Dancer's Beat now works with Critical Attacks. | **요구조건**: `{'stats': {'Power': 15}, 'objectives': ['Purchase in Shop'], 'memento': 'Spear Dancer'}`

### Not My Tempo `[Memento]`
- **설명**: Dancer's Beat grants Hyperarmor. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Spear Dancer'}`

### Two Left Feet `[Memento]`
- **설명**: Posture breaking an opponent grants you +50% PEN for 3 seconds. | **요구조건**: `{'stats': {'Power': 10}, 'objectives': ['Purchase in Shop'], 'memento': 'Spear Dancer'}`
- **추가 정보**: 14 second cooldown.

### Ignition Rite `[Memento]`
- **설명**: Landing fire attacks with the phoenix summoned regenerates Heartfire. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Solborn'}`

### Heartfire Renewal `[Memento]`
- **설명**: Regenerate Heartfire whenever you are burning. Upon revival with Phoenix Flames, restore half of your Heartfire gauge. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Solborn'}`

### Solborn `[Memento]`
- **설명**: Harness your Heartfire to command the Phoenix bound to your soul. | **요구조건**: `{'memento': 'Solborn'}`
- **추가 정보**: Spawns a small orange, stationary, Phoenix near you. The size of the Phoenix will increase based on the user's level. This Phoenix can be used like a campfire to rest and heal yourself.

### Explosive Ignition `[Memento]`
- **설명**: Ignite nearby steam, causing a large explosion. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Steampunk Soldier'}`
- **추가 정보**: Grants a Talent tool, that when used while standing inside of a steam cloud causes a very large explosion after a delay, dealing high damage and consuming the Steam cloud.

### Mist Mobility `[Memento]`
- **설명**: Anytime you proc Boiling Point, increase the speed at which you reload your Vapormaw Carbine and increase your Critical Attack's fire rate. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Steampunk Soldier'}`
- **추가 정보**: Despite what the description states, this actually procs when you activate Flashboil, and not Boiling Point.

### Steampunk Soldier `[Memento]`
- **설명**:  Increase the size of your steam which you activate Flashboil. Flashboil's cooldown is also reduced. | **요구조건**: `{'memento': 'Steampunk Soldier'}`

### Alloy Siphon `[Memento]`
- **설명**:  Iron Pull siphons armor from your foes, restoring your posture. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Iron Vessel'}`

### Steelvessel `[Memento]`
- **설명**: Landed attacks deal posture damage but when guard broken take massive damage. Posture gain on parry is reduced. | **요구조건**: `{'memento': 'Iron Vessel'}`
- **추가 정보**: Take posture damage instead of health damage. Upon being guardbroken, take a large amount of damage to your healthbar. Your healing and posture restoration from parrying attacks is reduced.

### Magic Coffin `[Memento]`
- **설명**: A jack of all trades, all attribute requirements are ignored. Activate your Coffin with C. | **요구조건**: `{'memento': 'Strange Merchant'}`
- **추가 정보**: Activating your Coffin takes 50 Notes. This Note cost will increase by 50 per Power, costing 1,000 Notes at Power 20. When used, the Coffin acts like a loot box, randomly rolling an item to give you. There is a 1% chance to grant the Skull, giving you high tier loot. This chance is increased by 1% per level, up to 20% at power 20. There is a 5-10% chance to roll a blank, doubling the chest of the next box. This can stack. Coffin activation uses your Resonance keybind. You can use any weapon or equipment item without meeting their attribute requirements.

### True Mirage Clone `[Rare]`
- **설명**: Successfully dodging leaves behind a heat mirage clone that sets enemies that swung at you on fire. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Flame Worshipper'}`
- **추가 정보**: 20 second cooldown.

### Spark of Theros `[Memento]`
- **설명**: Your Thundercall is imbued with the spark of Theros, altering its appearance and properties. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Theros Disciple'}`
- **추가 정보**: Turns your Thundercall white and changes your Shock to Blightshock, applying Wither to affected targets.

### Storm Return `[Memento]`
- **설명**: Being under lightning/wind status effect causes your Basic Attacks and Criticals to do 10% more damage. (Amplified with Lightning Cloak) | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Theros Disciple'}`
- **추가 정보**: Being under the effects of Amped or Lightning Cloak will proc this effect.

### Compelling Offer `[Memento]`
- **설명**: Any charmed enemy below 50% hit with your mantras or critical will mysteriously begin attacking everyone but you. [Madness] Your taunt also now functions as a counter that stacks damage multipliers with every successful taunt. | **요구조건**: `{'objectives': ['Purchase in Shop'], 'memento': 'Strange Merchant'}`
- **추가 정보**: Madness from this Talent procs when attacking charmed enemies who are below 50% health. Using Taunt as a counter displays Prediction's visual effects but with a dark purple color. This also plays a laughing sound effect and reduces Taunt's cooldown to 1 second. Taunt counter does not deal damage, but instead stacks Taunt's damage buff effect.

### Jackpot `[Common]`
- **설명**: Charmed enemies now have a chance to be hit critically, multiplying the damage. | **요구조건**: `{'stats': {'Power': 20}, 'objectives': ['Purchase in Shop'], 'memento': 'Strange Merchant'}`

### Sweeten the Deal `[Memento]`
- **설명**: Madness can now be applied to enemies at 80% health or lower. | **요구조건**: `{'stats': {'Power': 10}, 'objectives': ['Purchase in Shop'], 'memento': 'Strange Merchant'}`

### Taunting Tongue `[Common]`
- **설명**: Your taunt now applies Madness.

### Voice of the Mad God `[Common]`
- **설명**: Any time you apply charm it now applies "Madness" to enemies directly. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Strange Merchant'}`

### Precision Hitter `[Memento]`
- **설명**: Your Basic Attack posture damage is increased by 15%. | **요구조건**: `{'stats': {'Power': 5}, 'objectives': ['Purchase in Shop'], 'memento': 'Saint Jay'}`

### Void Glutton `[Memento]`
- **설명**: Siphon some of your enemies ether when you kill them. This gets added onto your health permanently, however you are now slowed at all times. This slow increases the more health you have siphoned. | **요구조건**: `{'memento': 'Void Glutton'}`
- **추가 정보**: Gives 2 maximum health when you kill a player. You will also be slowed, with the slow being based on how much maximum health you've siphoned.

### Dark Harvest `[Memento]`
- **설명**: Steal all of the hunger of enemies caught in your Shadow Vortex. Knocking a player also greatly enhances your next Shadow Vortex. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Void Glutton'}`

### Erupting Shade `[Memento]`
- **설명**: The size of your shadow eruption increases with how much siphoned health you have gained from wiping players. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Void Glutton'}`

### Ether Repletion `[Memento]`
- **설명**: Hunger stolen from other players now grants you ether as well. | **요구조건**: `{'slay': 'True Heart of Enmity', 'memento': 'Void Glutton'}`
- **추가 정보**: Hunger stolen from players through any means will proc this Talent.

### Hearty Ether `[Memento]`
- **설명**: Devouring Eye steal procs now heal you based on the amount of ether stolen. | **요구조건**: `{'slay': 'Dravik, The Rat King', 'memento': 'Void Glutton'}`

### Null Recovery `[Memento]`
- **설명**: Sacrifice 20% of your hunger bar to recover 10% of your health back. | **요구조건**: `{'slay': "Shogun of the Prophet's Guard", 'memento': 'Void Glutton'}`

### Pleeksty's Inheritance `[Memento]`
- **설명**: You inherit the teachings of Amorus Pleeksty, augmenting your flamecharm mantras. | **요구조건**: `{'memento': 'Flame Worshipper'}`
- **추가 정보**: Makes your Flamecharm Mantras extremely loud.

### Blade Threading `[Weapon]`
- **설명**: Your Metal Greatsword now has Metal Fakeout as its critical attack. Landing Critical attacks applies metal rod and slow. | **요구조건**: `{'weapon': 'Ferractine'}`
- **추가 정보**: The Metal Fakeout critical will only be used while you are in targeting range. Additionally, this attack has innate Bleed and counts as a weapon attack, not a Mantra.

### Hex Bullet `[Weapon]`
- **설명**: Bullets that hit your opponents block shatter into dust on impact, unleashing a maddening smoke that increases your opponent's sanity. | **요구조건**: `{'weapon': 'Duskshot'}`

### Monster Slayer `[Weapon]`
- **설명**: Deal 25% more damage to giant enemies. | **요구조건**: `{'weapon': 'Darksteel Cleaver'}`

### Night Night `[Weapon]`
- **설명**: Uppercut attacks blind opponents for 15 seconds. | **요구조건**: `{'weapon': 'Night Star'}`

### Reforged Alloy `[Weapon]`
- **설명**: Anytime you consume iron rods using Metal Pull or any Rending Needle technique, reduce the cooldown of your next critical based on the amount of rods consumed.

### Reverse Necrosis `[Weapon]`
- **설명**: Landing any mantra will now heal you based on how slow your opponent is. | **요구조건**: `{'weapon': "Saint Jay's Hammer"}`

### Sadistic Split `[Weapon]`
- **설명**: Guardbreaking your opponent now heals you. The amount of this heal is based on how much insanity your character currently has. | **요구조건**: `{'weapon': 'Depthsplitter'}`

### Shatter `[Weapon]`
- **설명**: Landing a critical shatters your opponent, ridding them of their speed debuffs for 5 frost damage per debuff. | **요구조건**: `{'weapon': 'Icepick'}`
- **추가 정보**: Landing a critical attack removes all speed debuffs your opponent has, dealing 5 Frostdraw damage per debuff.

### Analyze `[Equipment]`
- **설명**: Marking enemies with your Callout analyzes them, making them take 20% more damage from all sources for 10 seconds. | **요구조건**: `{'equipment': 'Armored Sensor Mask'}`
- **추가 정보**: 45 second cooldown.

### Beginner's Luck `[Equipment]`
- **설명**: Slightly increase the amount of loot you find in chests. | **요구조건**: `{'equipment': "Beginner's Brace"}`

### Blend In `[Equipment]`
- **설명**: You resemble one of the Enforcers, become unnoticeable by regular depths mobs. | **요구조건**: `{'equipment': 'Enforcer Helm'}`
- **추가 정보**: Most monsters in the Depths will be neutral you while you have this equipment on.

### Blood Siphon `[Equipment]`
- **설명**: Your Critical Attack now siphons a bit of health, healing you 10% of the damage you dealt. | **요구조건**: `{'equipment': 'Bloodcurdle Cowl'}`

### Clutch `[Equipment]`
- **설명**: For every combat tag you acquire, gain 4% more posture resistance. | **요구조건**: `{'equipment': 'Reinforced Authority Plate'}`

### Conditioning `[Equipment]`
- **설명**: Reduce all slows you receive by 40%. | **요구조건**: `{'equipment': "Veteran Ranger's Boots"}`

### Cursed Immortality `[Equipment]`
- **설명**: Instead of getting knocked, get set to 75% health. When this effect occurs, this guarantees that you depths trial will become corrupted for the rest of your character's run. | **요구조건**: `{'equipment': 'Corrupted Immortal Helm'}`
- **추가 정보**: Instead of being knocked, your health will be set to 75% of its maximum instead, with a 5 minute cooldown. Once this Talent procs, all future Depths trials will automatically be corrupted for the rest of your character's life. This Talent does not proc during the Zi'eer boss fight.

### Emergency Rations `[Equipment]`
- **설명**: Eat some of your emergency rations, healing you for 20 health. You can only use this 3 times before having to sit at a campfire outside of combat again. | **요구조건**: `{'equipment': "Veteran Ranger's Brace"}`
- **추가 정보**: Grants a Talent tool with 3 charges. Using the Talent tool consumes one of the charges to heal you for 20 flat health. This has a 15 second cooldown. Resting at a campfire, while not in combat, restores all charges

### Ether Efficiency `[Equipment]`
- **설명**: All mantras you cast now have a reduced cost of 30 ether. | **요구조건**: `{'equipment': 'Caster Fur Boots'}`

### Ether Upgrade `[Equipment]`
- **설명**: All mantras you cast now get one bonus level on top of their current level. | **요구조건**: `{'equipment': 'Caster Fur Pauldrons'}`

### Experienced Healer `[Equipment]`
- **설명**: Everytime you heal yourself, gain 5 extra health on top of that. | **요구조건**: `{'equipment': 'Cultist Cowl'}`
- **추가 정보**: 10 second cooldown.

### Fictitious Force `[Equipment]`
- **설명**: Reduce the power of all speed boosts you gain by 50%. Deal extra true damage based on how fast you are. | **요구조건**: `{'equipment': "Corrupted Duelist's Mask"}`
- **추가 정보**: Halves the effectiveness of all speed boosts. Adds true damage to your attacks, with the true damage scaling on your speed boosts and momentum.

### Flare Drop `[Equipment]`
- **설명**: Landing mantras sets your opponent on fire. | **요구조건**: `{'equipment': 'Flare Drop Earrings'}`
- **추가 정보**: Applies burn when you land a Mantra with a 5 second cooldown.

### Flask Amplifier `[Equipment]`
- **설명**: Heal an extra 15% from flasks. | **요구조건**: `{'equipment': "Potion Master's Hat"}`
- **추가 정보**: Increases the healing gained from Etris Flasks by 15% additively, meaning Flasks will restore 65% health on use instead of 50%.

### Gale Boots `[Equipment]`
- **설명**: Reduce the amount of fall damage you take by 50%. | **요구조건**: `{'equipment': 'Gale Boots'}`

### Gunslinger's Fury `[Equipment]`
- **설명**: When having a side gun equipped with a gun or rifle, use a critical in the air to shoot a barrage of bullets towards your opponent. | **요구조건**: `{'equipment': "Bounty Hunter's Boots"}`
- **추가 정보**: If your main weapon is a Pistol or a Rifle, and you have an offhand Pistol equipped, your critical will be replaced with the Soulwrought Gun's special attack if used midair.

### Haste `[Equipment]`
- **설명**: Gain a permanent +3 speed buff at all times. | **요구조건**: `{'equipment': 'Trackstar Boots'}`
- **추가 정보**: Increases your movement speed by +3 studs per second. This does not count as a speed boost for Talent procs.

### Hellion Shift `[Equipment]`
- **설명**: The more insane you are the more iframes you gain on your dodge. | **요구조건**: `{'equipment': 'Oni Mask'}`

### Heretic's Sacrifice `[Equipment]`
- **설명**: A chant that heavily sacrifices your sanity to regain a bit of health. | **요구조건**: `{'equipment': "Heretic's Moonseye Gauntlets"}`
- **추가 정보**: Grants a Talent tool that drains a significant amount of sanity to heal 20 raw health. If you are already at 0 Sanity, you will still be healed at no downside.

### Iron Stance `[Equipment]`
- **설명**: Be able to shrug off being ragdolled every so often. | **요구조건**: `{'equipment': "Depths Wanderer's Boots"}`
- **추가 정보**: Grants immunity to one instance of ragdoll. If this procs, it will go on a 20 second cooldown.

### Navae's Conviction `[Equipment]`
- **설명**: All Navaen related combat weapons are empowered. | **요구조건**: `{'equipment': 'Blessed Nomad Pendant'}`

### Natural Healing `[Equipment]`
- **설명**: Every time you eat plants, heal 2% of your health. | **요구조건**: `{'equipment': "Lifeweaver's Hat"}`
- **추가 정보**: "Plants" refers to any plant-based food item.

### Omen `[Equipment]`
- **설명**: Your Shadow Travel now has no windup and always requires health to teleport. | **요구조건**: `{'equipment': 'Corrupted Pathfinder Elite'}`

### Pace `[Equipment]`
- **설명**: Hitting opponents apply a speed boost. The faster you are the less damage you take. | **요구조건**: `{'equipment': 'Trackstar Pauldrons'}`
- **추가 정보**: Grants damage reduction based on the combined potency on all speed boosts you have. Landing attacks grants a speed boost.

### Piercing Shot `[Equipment]`
- **설명**: Activate to make your next critical attack with any gun have 100% chip and shatter your opponent's armor for a few seconds, making them take increased PEN from all sources. | **요구조건**: `{'equipment': "Bounty Hunter's Garb"}`
- **추가 정보**: Grants a Talent tool, that on use, enhances your next critical attack used with any Rifle or Pistol. Enhanced critical attacks gain 100% chip damage and apply the Pierced Armor status effect to your opponent, increasing incoming PEN for a few seconds.

### Poisoned Knife `[Equipment]`
- **설명**: Your Deepwound's anti heal now lasts 60 seconds on assassination instead of 20. | **요구조건**: `{'equipment': "Rogue Assassin's Hood"}`

### Pyreborne `[Equipment]`
- **설명**: Your Flamecharm mantras have all stats amplified. | **요구조건**: `{'equipment': 'Emberseal Pendant'}`
- **추가 정보**: Increases the base damage of all Flamecharm Mantras by 30%.

### Risky Defense `[Equipment]`
- **설명**: Decrease how much posture damage you take from physical attacks by 25%, but take 50% more posture damage from mantras. | **요구조건**: `{'equipment': 'Alloyed Phalanx Plate'}`
- **추가 정보**: Increases incoming posture damage from Mantras by 50%. Decreases incoming posture damage from weapon attacks by 25%.

### Royal Charge `[Equipment]`
- **설명**: When landing a running attack while using a club to gain a bit of temp health. | **요구조건**: `{'equipment': 'Royal Commander Helm'}`
- **추가 정보**: Running attacks with Club weapons grant Temporary Health. 20 second cooldown.

### Safety First `[Equipment]`
- **설명**: At the start of fights, gain 25% damage resistance for 30 seconds. | **요구조건**: `{'equipment': "Beginner's Boots"}`

### Sky Aid `[Equipment]`
- **설명**: Take 80% less damage while in the air. | **요구조건**: `{'equipment': 'Sky Warrior Helm'}`

### Slick `[Equipment]`
- **설명**: Coat of the infamous thief Emiya Konga. Improves the user's sliding abilities. This effect stacks with Konga's Clutch Ring. | **요구조건**: `{'equipment': "Konga's Parka"}`

### Steel Grip `[Equipment]`
- **설명**: When you are blockbroken, negate it and set your posture to 80%. | **요구조건**: `{'equipment': 'Reforged Gauntlets'}`
- **추가 정보**: 90 second cooldown.

### Tempo Sap `[Equipment]`
- **설명**: Activate to make your dagger's light attacks steal tempo per hit for 20 seconds. [Dagger] | **요구조건**: `{'equipment': "Prophet's Operative Cloak"}`
- **추가 정보**: 1 minute cooldown.

### Tenacity `[Equipment]`
- **설명**: Greatly shorten the amount of time you are guardbroken for. | **요구조건**: `{'equipment': 'Hardened Barrel Helm'}`
- **추가 정보**: Reduces the stun duration from being guardbroken by 75%; from 1.05s to 0.26s.

### The Rich Get Richer `[Equipment]`
- **설명**: Gain 15% more notes whenever you sell something. | **요구조건**: `{'equipment': 'Prosperous Gumshoe Longcoat'}`

### Vessel's Gamble `[Equipment]`
- **설명**: When you get guardbroken you take 3 times the damage of the attack. | **요구조건**: `{'equipment': "Corrupted Vessel's Boots"}`
- **추가 정보**: Though this Talent is actively detrimental to the user, the Corrupted Vessel's Boots +20 Posture offsets the downside.

### Weather Resistant `[Equipment]`
- **설명**: Take 30% less damage when under less than ideal weather conditions. | **요구조건**: `{'equipment': 'Extra Thick Overcoat'}`

### Explosive Rounds `[Equipment]`
- **설명**: Every bullet that lands now detonates on your opponent. | **요구조건**: `{'set': 'Bounty Hunter'}`

### Hunting Trap `[Equipment]`
- **설명**: Place down a trap that upon being stepped on will render your opponent unable to move for a bit. | **요구조건**: `{'set': 'Veteran Ranger'}`
- **추가 정보**: Grants a Talent tool that places a bear trap on use. 60 second cooldown. Walking onto a bear trap deals high damage and renders you immobile for a few seconds. The bear trap cannot trigger again once it has been triggered. You can trigger your own bear trap.

### Overdrive `[Equipment]`
- **설명**: Go beyond your limits. All mantras you cast deal twice as much damage for 10 seconds. | **요구조건**: `{'set': 'Caster Fur'}`
- **추가 정보**: Grants a Talent tool that doubles the damage of your Mantras for 10 seconds. 3 minute cooldown.

### Rush `[Equipment]`
- **설명**: Massively reduce your dodge cooldown. | **요구조건**: `{'set': 'Trackstar'}`

### Training Wheels `[Equipment]`
- **설명**: Increase the amount of parry frames you have by 20%. | **요구조건**: `{'set': 'Beginner'}`

### Unyielding Frost `[Advanced]`
- **설명**: Your Chilled can proc through block, with blocked Chilled procs lasting 80% of the duration. | **요구조건**: `{'stats': {'Frostdraw': 100}}`
- **추가 정보**: If you have less than 100 Frostdraw, your Chill duration (when applied through block) will be reduced down to 25% of its original duration instead.

### Unyielding Inferno `[Common]`
- **설명**: Your flames burn just as strong even in the fiercest of storms. | **요구조건**: `{'stats': {'Flamecharm': 35}}`
- **추가 정보**: Negates the innate 10% damage debuff Flamecharm Mantras, First Light's critical, and Twisted Puppets' Puppets receive during the rain. Prevents your burn from being extinguished by the rain.

### Oath: Saltchemist `[Oath]`
- **설명**: You vow to dedicate body and mind to the furthering of the Material Arts. Your body is a conduit through which true knowledge shall be siphoned. Knowledge is power, and you shall be its vessel. | **요구조건**: `{'stats': {'Intelligence': 75}, 'objectives': ["Complete Ciea's Quest once"]}`

### Swiftkick Prodigy `[Common]`
- **설명**: Hitting successive Basic Attacks with Jus Karita will give a temporary speed buff. | **요구조건**: `{'talents': ['Jus Karita']}`
- **추가 정보**: Your third M1 will grant a speed boost for a short duration.

### Ankle Cutter `[Oath]`
- **설명**: You can now do a special ground slash while sliding, applying a temporary speed debuff to those hit, as well as preventing jumping. | **요구조건**: `{'talents': ['Oath: Silentheart'], 'or': [{'slay': 'X amount of Attunement Trainers'}, {'objectives': ['Pay 10 Knowledge to the Dreadstar']}]}`
- **추가 정보**: Deals 37.5 Oath damage. If in Flow State, this is increased to 52.5 and the windup is reduced. Has innate bleed. 6 second cooldown.

### Piercing Will `[Rare]`
- **설명**: When your sanity is below 35%, gain up to +15% PEN on your attacks. Starting at 5% PEN, the lower your sanity, the higher your PEN. | **요구조건**: `{'stats': {'Willpower': 80}}`
- **추가 정보**: Grants a 10% PEN bonus at full insanity despite what the description states. The bonus PEN is applied starting from 35% Sanity.

### Ancient Metalwork `[Weapon]`
- **설명**: Your critical hit can channel the effects of your Ironsing Rods and disrupt the resonances of others, disabling them for 25 seconds. | **요구조건**: `{'weapon': 'Dissonant Chimecaller'}`
- **추가 정보**: Landing your weapon critical puts your opponent's Resonance on a 25 second cooldown.

### Both Ends `[Weapon]`
- **설명**: Pressing M2 after landing a light attack with the staff performs a follow-up swing from the opposite end. | **요구조건**: `{'or': [{'weapon': 'Wooden Staff'}, {'weapon': 'Duskpole'}, {'weapon': 'Imperial Staff'}, {'weapon': 'Sancticar'}]}`
- **추가 정보**: The followup attack has fast swing speed, but it only deals 45% of your weapon damage.

### Counter Spin `[Common]`
- **설명**: After blocking an attack, press M2 to counter with your staff. | **요구조건**: `{'stats': {'Medium Weapon': 35}, 'weaponType': 'Staff'}`
- **추가 정보**: On proc, swiftly thrust your Staff forwards, dealing 45% of your weapon's damage on hit.

### Breakthrough Drive `[Faction]`
- **설명**: Knocking a player refreshes your Glorious Charge cooldown and extends both effects it has by 5 seconds. [90 second CD] | **요구조건**: `{'objectives': ['Command Division'], 'origin': 'Authority Ensign'}`

### Slider Style `[Weapon]`
- **설명**: Raise the cap of how fast you are able to slide. Your Jus Karita fighting style gains a new sliding crit. Its power stems from how fast you are sliding when using the critical attack.

### Stasis Strike `[Common]`
- **설명**: Your crystal explosions deal more damage whenever your opponent is also bottom frozen. | **요구조건**: `{'stats': {'Weapon': 90, 'Frostdraw': 90}, 'talents': ['Glass Path: Crystallization']}`
- **추가 정보**: Stasis Strike increases the damage of your crystal explosions by 1.67x when your opponent is bottom frozen.

### Decisive Blow `[Common]`
- **설명**: Hitting an enemy with your Critical Attack immediately after they dodge (or any time against mobs) now procs Knife's Journey. Your Knife's Journey procs do 2x Armor damage. | **요구조건**: `{'talents': ["Knife's Journey"]}`

### Karita Combo `[Faction]`
- **설명**: Remove the endlag from your next running attack. [5 second CD] Landing a critical attack right after your running attack makes that critical attack have no cooldown and deal more damage. [10 second CD] | **요구조건**: `{'talents': ["Justicar's Technique"], 'objectives': ['Vanguard Path'], 'origin': 'Justicar'}`

### Righteous Crash `[Faction]`
- **설명**: Slamming down your opponent in the air with a flourish or your upgraded Vanguard Jus Karita critical deals extra true damage based on high up in the air they were. | **요구조건**: `{'objectives': ['Vanguard Path'], 'origin': 'Justicar'}`

### Swiftkick Master `[Faction]`
- **설명**: Proccing Swiftkick Prodigy now extends its duration to 15 seconds. | **요구조건**: `{'talents': ['Swiftkick Prodigy'], 'objectives': ['Vanguard Path'], 'origin': 'Justicar'}`

### Soaring Swiftkick `[Faction]`
- **설명**: Flying Swiftkick no longer consumes your speed boost and instead gives you more speed. | **요구조건**: `{'talents': ['Flying Swiftkick'], 'objectives': ['Vanguard Path'], 'origin': 'Justicar'}`

### Vanguard Style `[Faction]`
- **설명**: When using the Jus Karita critical attack, turn it into a kick that brings your enemies up in the air. Landing the critical attack while your opponent is in the air brings them up and slightly stun them while upgrading your next critical. | **요구조건**: `{'objectives': ['Vanguard Path'], 'origin': 'Justicar'}`
- **추가 정보**: This new critical attack has 20 base damage with no investment scaling.

### Vanguard's Onslaught `[Faction]`
- **설명**: Landing a Vanguard Style Jus Karita critical attack makes you deal 20% more damage in the air for the next 5 seconds. | **요구조건**: `{'objectives': ['Vanguard Path'], 'origin': 'Justicar'}`

### Justicar's Mark `[Faction]`
- **설명**: Mark someone you wish to protect for a minute. While marked, you take 20% of the damage they receive but they take 20% less damage. Marking someone also cause you to take 20% more damage while they are marked. | **요구조건**: `{'objectives': ['Warder Path'], 'origin': 'Justicar'}`
- **추가 정보**: Grants a Talent tool that allows you to apply the Justicar's Mark status effect on one of your allies. While this effect is active, the marked target gains 20% damage redirection, as 20% of the damage they would have taken is redirected to you instead. Additionally, you take 20% more damage.

### Kindness `[Faction]`
- **설명**: Whenever you heal another player, heal 5 health yourself. | **요구조건**: `{'objectives': ['Warder Path'], 'origin': 'Justicar'}`
- **추가 정보**: 3 second cooldown.

### Righteous Violence `[Faction]`
- **설명**: Landing a Critical Attack heals your marked ally. Landing a Jus Karita critical or Karita Swap heals your marked ally even more. | **요구조건**: `{'talents': ["Justicar's Mark"], 'objectives': ['Warder Path'], 'origin': 'Justicar'}`

### Mark Mastery `[Faction]`
- **설명**: Reduce the amount of extra damage you receive while your ally is marked with the Justicar's Mark from 20% to 5%. | **요구조건**: `{'talents': ["Justicar's Mark"], 'objectives': ['Warder Path'], 'origin': 'Justicar'}`
- **추가 정보**: Reduces the additional damage you take from marking an ally from 20% to 5%.

### Justicar's Blessing `[Faction]`
- **설명**: Allies you mark with Justicar's Mark gain 15% more healing. | **요구조건**: `{'talents': ["Justicar's Mark"], 'objectives': ['Warder Path'], 'origin': 'Justicar'}`

### Emergency Mark `[Faction]`
- **설명**: Applying a mark on someone who has less than 20% health heals them for 10% of their health. | **요구조건**: `{'talents': ["Justicar's Mark"], 'objectives': ['Warder Path'], 'origin': 'Justicar'}`
- **추가 정보**: Applying a Justicar's Mark on an ally who has 20% or less current health health them for 10% of their maximum health.

### Trained Legs `[Faction]`
- **설명**: Slightly increase your climb strength. | **요구조건**: `{'origin': 'Justicar'}`
- **추가 정보**: Increases your maximum climb height.

### Swiftfoot `[Faction]`
- **설명**: Reduce all slows you receive by 10%. | **요구조건**: `{'origin': 'Justicar'}`

### Marked Descent `[Faction]`
- **설명**: When your Justicar's Mark target takes damage, they are revealed. Using your Karita Divebomb will target them. | **요구조건**: `{'talents': ["Justicar's Mark"], 'objectives': ['Warder Path'], 'origin': 'Justicar'}`
- **추가 정보**: Targets the enemy who hit your marked ally, not the marked ally themselves.

### Justicar's Preference `[Faction]`
- **설명**: Replace your critical with the Jus Karita critical attack. | **요구조건**: `{'origin': 'Justicar'}`
- **추가 정보**: The Jus Karita critical will adopt your equipped weapon's scaling stat.

Having the Vanguard Style Talent will override this Talent, allowing you to use the Vanguard Style critical on any weapon instead of the default Jus Karita one.

### Justicar's Adaptation `[Faction]`
- **설명**: Jus Karita running attacks and criticals can now proc Jus Karita talents even if you aren't currently using Jus Karita. Your Jus Karita running attacks can now also proc fist talents. | **요구조건**: `{'origin': 'Justicar'}`
- **추가 정보**: This Talent synergizes extremely well with Justicar's Preference and Justicar's Technique, allowing you to proc the effects of this Talent on any weapon.

### Justicar's Technique `[Faction]`
- **설명**: Replace your running light attack with the Jus Karita running light attack. With the Justicar's Training, your legs extend the range of this running attack by an extra 0.5. | **요구조건**: `{'origin': 'Justicar'}`
- **추가 정보**: Replaces your weapon's running attack animation with the Jus Karita one, and adds 0.5 range to your running attacks.

### Justicar's Gift `[Outfit]`
- **설명**: Your Justicar support mantras now heal your allies for 10 health instead of 5. Increase the duration of your Karita Aid to 15 seconds. | **요구조건**: `{'outfit': "Warder's Attire"}`

### Unstoppable Force `[Rare]`
- **설명**: [Greathammer] You take 15% less posture damage when parried. | **요구조건**: `{'stats': {'Strength': 25, 'Heavy Weapon': 40}, 'talents': ['Unwavering Resolve'], 'weaponType': 'Greathammer'}`

### Vacuum Punch `[Common]`
- **설명**: Your Gale Punch pulls enemies in before you hit them. | **요구조건**: `{'stats': {'Galebreathe': 20}, 'mantras': ['Gale Punch']}`
- **추가 정보**: Gale Punch Mantra will now pull players towards the user during the windup of the Mantra. Increases Gale Punch's windup by 0.1s.

### Scorchblood `[Common]`
- **설명**: Guardbreaking your opponent using a bloodrend mantra causes a blood explosion, setting your opponent on fire and poisoning their blood. | **요구조건**: `{'stats': {'Bloodrend': 40, 'Flamecharm': 40}}`
- **추가 정보**: Deals 16.5 damage in an AoE on proc.

### Dark Replenishment `[Common]`
- **설명**: Knocking out an enemy in combat restores a portion of your ether. | **요구조건**: `{'stats': {'Shadowcast': 50, 'Intelligence': 25}, 'talents': ['Dark God']}`

### Strength Unbounded `[Common]`
- **설명**: You have gained the ability to surpass your limits and train your Strength to its fullest. | **요구조건**: `{'stats': {'Strength': 75}, 'objectives': ['Speak to Tolkat']}`
- **추가 정보**: Removes the 75 investment cap on the Strength Attribute. The stat requirements to obtain this Talent will be increased to 77 or 78 if your Aspect has increased Strength on spawn, though this limitation will be removed if you have the Multifaceted Echo Unlock. The quest requirement for this Talent will be removed if you've obtained it previously on your account.

### Beiruul's Vengeance `[Quest]`
- **설명**: Deal 5% more damage to factions that despise you. Serves them right. | **요구조건**: `{'quests': ["Navae's Retribution"]}`

### Another Man's Trash `[Advanced]`
- **설명**: Take unequipped equipment when mugging a player. Gain a little more damage against PvE the more you are currently carrying. | **요구조건**: `{'stats': {'Charisma': 35, 'Agility': 10}, 'talents': ['Cap Artist', 'Pickpocket']}`
- **추가 정보**: If the player you are mugging doesn't have any Notes, you will still take any unequipped equipment. You cannot steal Soulbound or Enchanted items. Gain +0.001% damage for every 1 Weight you're carrying. Every 100 Weight = +1% damage.

### Mantra Permanence `[Common]`
- **설명**: Knocking an enemy with a mantra refunds the cost of the mantra. | **요구조건**: `{'stats': {'Intelligence': 20}}`

### Ironclad Punishment `[Common]`
- **설명**: Your Ironsing mantras deal more posture damage to enemies the more armor durability they have. | **요구조건**: `{'stats': {'Ironsing': 45}}`
- **추가 정보**: Gain +0.15% posture damage on Ironsing Mantras for every 1% armor durability your opponent has, capping at +15% if your opponent is at maximum armor.

### Ether Proselyte `[Oath]`
- **설명**: All of your Elemental Mantras below Lv. 5 are now 1 level higher. Your Mantras are now converted to the element of your current stance. | **요구조건**: `{'talents': ['Oath: Saintsworn'], 'or': [{'slay': 'The Doom of Caeranthil'}, {'slay': 'Interluminary Parasol'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Increases the level of all Attuned Mantras by 1 unless they are already level 5. This is not displayed on the Mantra's tooltip. Allows your non-Ironsing/Bloodrend Attuned Mantras to proc the Attunement Talents of your current Saint Stance. (E.g. Clutching Shadow in the Flamecharm Stance can proc Scorched Peak). Not all Attuned Talents are compatible with Ether Proselyte.

### Hero's Assist `[Oath]`
- **설명**: Heroes come to your aid based on your current stance. | **요구조건**: `{'talents': ['Oath: Saintsworn'], 'or': [{'slay': 'The Doom of Caeranthil'}, {'slay': 'Interluminary Parasol'}, {'objectives': ['Pay 10 Knowledge']}]}`
- **추가 정보**: Each Saint has a specific spawn requirement and ability when spawned. You can spawn heroes independent of your current Saint Stance. This passive ability works once per Saint Stance, requiring you to cycle to the next one to reactivate.

### Perpetual Distillery `[Oath]`
- **설명**: Your very body has become a distillery for your alchemy. Gain 3 Autobrew slots that will automatically produce 3 concoctions of your choice. | **요구조건**: `{'talents': ['Oath: Saltchemist']}`
- **추가 정보**: Upon using the Distillery's Talent tool, you're given three empty spaces where you input your potions. You're able to switch the mode from "Throw" to "Drink", and vice versa. Each potion in the Distillery will be given as a Talent tool, using the potion on use. Potions in the Distillery go on cooldown when used. Drink potions place other drink slots on a cooldown if they share buffs.

### Unnecessary Theatrics `[Common]`
- **설명**: Deliver a one-liner on uppercuts, flourishes and critical attacks that charms your opponents briefly. | **요구조건**: `{'stats': {'Charisma': 75}, 'talents': ['Charismatic Cast']}`
- **추가 정보**: The charm proc has no cooldown, but the one-liners do. Instantly reapplies Charm after Manipulator removes it, on the same hit.

### Bulletproof `[Common]`
- **설명**: You take no Armor damage from guns. You take 5% less Armor damage from other sources. | **요구조건**: `{'quests': ['Trig Quest'], 'or': [{'stats': {'Fortitude': 20}}, {'stats': {'Weapon': 20}}]}`
- **추가 정보**: This has no effect on your natural armor or incoming PEN.

### Oh The Irony `[Common]`
- **설명**: Opponents affected by 'Taunt' receive double iron rods for the duration. | **요구조건**: `{'stats': {'Ironsing': 60, 'Charisma': 40}, 'mantras': ['Taunt']}`

### Taste The Rainbow `[Common]`
- **설명**: Every time you shoot, switch your ammo type. [Dual Guns] | **요구조건**: `{'stats': {'Light Weapon': 50}, 'weaponType': 'Pistol'}`

### Rule Through Fear `[Rare]`
- **설명**: Executing an enemy applies Overcharm to nearby allies and yourself. | **요구조건**: `{'stats': {'Charisma': 85, 'Strength': 50}}`
- **추가 정보**: Overcharms for 10 seconds.

### Merciless Blade `[Oath]`
- **설명**: Increases your Execution speed by 40%. | **요구조건**: `{'talents': ['Oath: Silentheart']}`
- **추가 정보**: Reduces the time it takes to successfully Execute down to 1.8 seconds from 3 seconds.

### Stratoshock `[Common]`
- **설명**: Your lightning deals an additional +5% damage when in the rain. | **요구조건**: `{'stats': {'Thundercall': 35}}`
- **추가 정보**: All sources of Thundercall damage innately gains a 5% damage buff if it is raining. This Talent adds an additional 5%.

### Apparitions `[Common]`
- **설명**: Your Haunted Phantoms become Apparitions that apply Winded on hit. Apparitions cannot be parried if you are in Phantom Step. | **요구조건**: `{'stats': {'Galebreathe': 50}, 'talents': ['Haunted Path: Specter']}`
- **추가 정보**: Apparitions can only spawn from Haunted Gale being procced on Galebreathe Mantras or by proccing effects that would normally apply Suffocation.

### Donation Drive `[Common]`
- **설명**: Consuming 'Charm' on an opponent replenishes some blood. Additionally, you can also activate this effect and Manipulator through blockbreaking with a Bloodrend mantra. | **요구조건**: `{'stats': {'Bloodrend': 50, 'Charisma': 55}, 'talents': ['Manipulator']}`
- **추가 정보**: Donation Drive's cooldown scales on your Charisma investment, having an 8 second cooldown at 60 Charisma and gaining 0.1s for every point in Charisma below 60. Donation Drive has a 8.5 second cooldown at 55 Charisma, and a maximum cooldown of 10.5 seconds at 35 Charisma.

### Fried Circuits `[Common]`
- **설명**: Overloading an enemy applies Sapped for 5s. | **요구조건**: `{'stats': {'Thundercall': 60}, 'talents': ['Surge Path: Unstable Capacitor']}`
- **추가 정보**: Targets affected by Sapped have the cooldowns of their Mantras increased.

### Enrage `[Common]`
- **설명**: Whenever you stun an opponent who's taunted with Encore, enrage them. | **요구조건**: `{'stats': {'Charisma': 65}, 'talents': ['Encore'], 'objectives': ['Wipe with the Strange Merchant Memento']}`

### Justicar Whistle `[Origin]`
- **설명**: Request aid from a Justicar. | **요구조건**: `{'or': [{'origin': 'Castaway'}, {'origin': 'Lone Warrior'}, {'origin': 'Deepbound'}]}`
- **추가 정보**: Upon using the provided Talent tool, a Justicar may respond to your call for aid, teleporting to your server to assist you with events and protect you in combat. If you are a Lone Warrior or Deepbound, you will lose access to the Whistle at Power 16.

### Justicar's Call `[Origin]`
- **설명**: Lend your aid to those in need.
- **추가 정보**: Upon using the provided Talent tool, a UI will pop up that shows a list of all Castaways who have used the Justicar Whistle tool. Upon selecting one, you'll teleport into their server, and you'll be tasked with protecting them against Voidwalkers and assisting them in events. Assisting Castaways with this tool is the main progression method of this Origin.

### Sacred Aura `[Weapon]`
- **설명**: Landing your Sacred Hammer critical attack applies an aura of protection around you, reducing the damage you take by a flat 2.5, multiplying based on how many combat tags you currently have on you. | **요구조건**: `{'weapon': 'Sacred Hammer'}`

### Continuous Bleed `[Weapon]`
- **설명**: Every time you land a crit, flourish, or uppercut, increase the amount of bleed damage you deal for 15 seconds. This is stackable. | **요구조건**: `{'weapon': 'Razor Cutlass'}`
- **추가 정보**: Reduces your bleed damage per tick by 5%, while adding an additional bleed damage tick per stack. This results in a net increase of ~26.7% more bleed damage for the first stack, with slightly diminishing returns for every stack you gain. Each stack has an independant duration, and stack gain has a 1.5 second cooldown.

### Rage Amp `[Weapon]`
- **설명**: At 2 or more combat tags, your critical now applies anti-heal while also increases the size and damage of your critical. This scales with the amount of combat tags you have. | **요구조건**: `{'weapon': 'Broodalloy Cestus'}`

### Ebb and Flow `[Weapon]`
- **설명**: Landing a medium mantra increases your heavy mantra's level by 1 and vice versa. This is stackable and can increased to a max of +5 levels. All stacks are removed if your medium/heavy mantra is defended against. | **요구조건**: `{'weapon': 'Wyrmtooth'}`

### Spinal Shatter `[Weapon]`
- **설명**: Landing the Crescent Cleaver critical attack causes your opponent to be unable to sprint for 8 seconds. [10 second CD] | **요구조건**: `{'weapon': 'Crescent Cleaver', 'or': [{'weapon': 'Alloyed Crescent Cleaver'}]}`

### Mudskipper Gripper `[Weapon]`
- **설명**: When executing an opponent with your critical attack, summon mudskippers to aid you in battle. | **요구조건**: `{'weapon': 'Coral Cestus'}`

### Terrapod Tracer `[Equipment]`
- **설명**: Deal 0.5% of your opponent's health to opponents who heal off of you. | **요구조건**: `{'equipment': 'Terraplate Pauldrons'}`
- **추가 정보**: This only works while your opponent has Anti-Heal.

### Broodlord's Scream `[Equipment]`
- **설명**: Using Sing, Taunt, or Ardour Scream applies anti heal for the duration of the move. | **요구조건**: `{'equipment': 'Broodplate Helmet'}`
- **추가 정보**: Applies 100% Anti-Heal. These abilities will also gain the Broodlord Scream sound effect.

### Overflow `[Outfit]`
- **설명**: Double the amount of tempo you receive when landing light attacks. | **요구조건**: `{'outfit': "Heretic's Memento"}`

### Cruentare `[Equipment]`
- **설명**: Increase the amount of all bleed damage you deal by 50%. Your Whirling Blade now now heals you when landing it. | **요구조건**: `{'equipment': 'Crimson Tetraplate Pauldrons'}`
- **추가 정보**: You heal for 25% of the damage your Whirling blades deals.

### Scorching Decay `[Common]`
- **설명**: The wither dealt from your Emperor's Flame is massively increased. | **요구조건**: `{'stats': {'Weapon': 100, 'Flamecharm': 100}, 'talents': ['Emperor Flame']}`
- **추가 정보**: Increases the Wither applied from Emperor Flame from 25 to 75.

### Mythic Stability `[Rare]`
- **설명**: Players and regular mobs cannot instantly execute you while you're on your feet. Protects you from one instance of instant execution while Unconscious. | **요구조건**: `{'stats': {'Fortitude': 85}}`
- **추가 정보**: 1 minute cooldown.

### Mercenary Blade `[Equipment]`
- **설명**: For every 10% stealth you have, deal 1 extra damage on all sources of damage. | **요구조건**: `{'equipment': "Mercenary's Hood"}`

### Stay of Execution `[Common]`
- **설명**: Increases the time taken to execute you by 20%. Saving others from being executed grants you both 10 TempHP (20s CD) | **요구조건**: `{'or': [{'stats': {'Charisma': 25}}, {'stats': {'Willpower': 25}}]}`

### Cook's Kit `[Common]`
- **설명**: Each food item's max quantity is increased by 5. Your kit comes with a lighter. | **요구조건**: `{'stats': {'Mind': 5, 'Fortitude': 5}}`
- **추가 정보**: You can light Campfires without a Flint.

### Chemistry Kit `[Common]`
- **설명**: You no longer drop potions on death. You have a 25% chance to brew an extra potion. | **요구조건**: `{'stats': {'Intelligence': 25}, 'objectives': ['Interact with a cauldron']}`

### Max Ammo `[Weapon]`
- **설명**: Landing the cannonball of your critical attack removes your critical attack's cooldown. | **요구조건**: `{'weapon': 'Summer Hullwrecker'}`

### Scammer `[Weapon]`
- **설명**: If your opponent tries to parry the fake hit of your critical attack, your critical attack will inflict a stronger daze upon your opponent. | **요구조건**: `{'weapon': "Scoundrel's Saber"}`

### Blade Scholar `[Weapon]`
- **설명**: Landing your fist critical attack switches your stance to that fist style. Retain the same swing speed and damage your Markor's Inheritor had. You gain more swingspeed the more Intelligence you have. | **요구조건**: `{'or': [{'weapon': "Markor's Inheritor"}, {'weapon': 'Alloyed Inheritor'}]}`
- **추가 정보**: Upon landing your critical, your weapon will swap to Iron Cestus/Anklets of Alsin for 15 seconds, retaining the base damage and swing speed of your Markor's Inheritor. Your investment scaling will be set to 7 Heavy Weapons (unaffected by Alloying your Inheritor), and 2 Intelligence while active. For every 1 Intelligence investment you have, gain an additional +0.002x swing speed while your weapon is Fists, allowing for 1.05x at 100 Intelligence. As this changes your weapon type, you will be able to proc Fist Talents while this effect is active. Enchantments carry over, but quality stars do not. If you do not have a Fist Style, you will equip Untrained Fists, which deals halved damage.

### One With Flame `[Outfit]`
- **설명**: When equipping a Worshipper Longsword and Worshipper Shield, you take 25% less damage while on fire and every mantra you use sets enemies on fire. | **요구조건**: `{'outfit': 'Flame Worshipper'}`
- **추가 정보**: These effects only apply while you are burning. Also turns your Medium Weapon Mantras orange and adds Flamecharm scaling to your Belief while active.

### Devastating Recovery `[Weapon]`
- **설명**: Enemies recover 30% less posture when parrying your Zweihander light attacks. | **요구조건**: `{'or': [{'weapon': 'Zweihander'}, {'weapon': 'Alloyed Zweihander'}, {'weapon': 'Bloodbane'}]}`

### Sweeping Edge `[Weapon]`
- **설명**: Your Master's Flourish is larger and can now proc flourish talents. | **요구조건**: `{'or': [{'weapon': 'Vigil Longsword'}, {'weapon': 'Alloyed Vigil Longsword'}]}`

### To The Finish `[Rare]`
- **설명**: You take 10% less damage when below 30% health. | **요구조건**: `{'stats': {'Fortitude': 50}}`
- **추가 정보**: For every point of Fortitude below 50, To the Finish loses 0.166% damage reduction, having a minimum value of 5.833% damage reduction at 25 Fortitude.

### Good Luck Charm `[Equipment]`
- **설명**: Makes you feel a little better, probably. | **요구조건**: `{'equipment': 'Jadeite Megalodaunt'}`

### Worshipper's Tolerance `[Weapon]`
- **설명**: Reduce the burn damage you take by 15%. While on fire, parrying an opponent's attack now sets them on fire [45 second CD]. | **요구조건**: `{'weapon': "Worshipper's Shield"}`

### Swift Blade `[Equipment]`
- **설명**: Proccing Wind Gem now gives you 10% more light attack posture during its duration. Extend the duration of Wind Gems by 2 seconds. | **요구조건**: `{'equipment': "Blademaster's Robe"}`

### Momentum `[Equipment]`
- **설명**: Speed boosts now give you a bit of extra chip based on how fast the speed boosts are making you. | **요구조건**: `{'set': 'Blademaster'}`

### Dancing Steps Of War `[Equipment]`
- **설명**: When landing a flourish, gain a speed boost and massively reduce the cooldown of your dodges for 2 seconds. | **요구조건**: `{'equipment': 'Geta'}`

### Blind Spot `[Equipment]`
- **설명**: [Land Critical Attack or Hidden Blade] Apply Blinded for 5 seconds. | **요구조건**: `{'equipment': "Inquisitor's Visor"}`
- **추가 정보**: 15 second cooldown.

### Thresher Thrasher `[Equipment]`
- **설명**: Adapt to the ways of the thresher, increasing how long you are able to stay underground with Beast Burrow by 30%, and reducing its cooldown by 25%. | **요구조건**: `{'equipment': 'Thresher Charm'}`

### Traditional Execution `[Equipment]`
- **설명**: Flourishing an opponent turns your next critical attack into the Katana critical attack. Also extends Dancing Steps Of War's effects by 0.5 seconds. | **요구조건**: `{'equipment': 'Etrean Sashimono'}`

### Champion's Shield `[Weapon]`
- **설명**: Deal an extra 25% more posture. Deal even more posture the more posture you have. | **요구조건**: `{'weapon': 'Icarus Sun Shield'}`
- **추가 정보**: Grants a +25% Posture damage buff. Additionally, grants a further Posture damage buff, scaling on the amount of Posture your character has.

### Propagandist `[Common]`
- **설명**: Your Sing will now stir your allies into a frenzy, causing them to become Overcharmed for 15s, applying Charmed to enemies they hit with Basic Attacks. | **요구조건**: `{'stats': {'Charisma': 75}, 'mantras': ['Sing']}`

### Gut Rot `[Equipment]`
- **설명**: Landing a flourish enhances your next instance of anti-heal, doubling its duration for how long it lasts. | **요구조건**: `{'equipment': 'Broodplate Sabatons'}`

### Second Nature `[Equipment]`
- **설명**: Ardour Scream no longer consumes ether and now instead adds 10 seconds to its cooldown. | **요구조건**: `{'set': 'Broodplate'}`

### Rotten Regeneration `[Equipment]`
- **설명**: Heal 20% more off enemies who have anti-heal on them. | **요구조건**: `{'equipment': 'Broodplate Cuirass'}`
- **추가 정보**: Grants increased offensive healing, such as from Bloodless Gems, when targeting enemies who are afflicted with Anti-Heal.

### Continuation `[Weapon]`
- **설명**: Everytime you swing your weapon, fire a series of slashes forward after that act as another light attack when landing. | **요구조건**: `{'weapon': 'Rangescraper'}`
- **추가 정보**: Light attacks fire projectiles that count as light attacks for other effects. This massively improves the weapon's range.

### Extension `[Weapon]`
- **설명**: For every hit you land with Rangescraper, extend the weapons range by 1 for 8 seconds. This effect stacks. | **요구조건**: `{'weapon': 'Rangescraper'}`

### Elemental Mentalist `[Common]`
- **설명**: Empower your Overcharm, allowing you and your allies to bring forth your high stat attunement's elemental effect into your light attacks when overcharmed. | **요구조건**: `{'stats': {'Charisma': 80, 'Intelligence': 40}, 'talents': ['Charismatic Cast']}`
- **추가 정보**: Applies to criticals with the M1 tag. When Overcharming yourself, your light attacks apply the status effect that correlates with your highest invested Attunement. When Overcharming your allies, their light attacks apply the the status effect that correlates to their highest invested Attunement. Does nothing if the Overcharmed party does not have an Attunement.

### Sclerosteosis `[Advanced]`
- **설명**: Anytime you lose 10% of your health in one hit, reduce the next instance of damage you take by 99%. [5 sec CD] | **요구조건**: `{'stats': {'Fortitude': 100}}`
- **추가 정보**: You need to take 10% of your maximum health as damage in a singular instance of damage for this effect to activate. The damage resistance is only applied when you get hit by weapon attacks or Mantras. Self damage can proc this effect.

### Camaraderie `[Weapon]`
- **설명**: Landing a critical attack reduce your allies' mantra cooldowns by 5 seconds and heals them 1%. [1 sec CD] | **요구조건**: `{'or': [{'weapon': 'Canorian Axe'}, {'weapon': 'Alloyed Canorian Axe'}]}`

### Swiftscales `[Weapon]`
- **설명**: Fang and Coil's base critical gains a small buff to its speed, range and endlag. | **요구조건**: `{'weapon': 'Steelscale Dusters'}`
- **추가 정보**: The increased range is telegraphed with a green version of the Fang and Coil critical vfx.

### Thread Ripper `[Weapon]`
- **설명**: When used by a Contractor, your Critical is empowered to eviscerate your opponents. | **요구조건**: `{'weapon': 'Palace Tachi'}`
- **추가 정보**: If the player is a Contractor, the Palace Tachi critical will autogrip knocked or low health targets.
