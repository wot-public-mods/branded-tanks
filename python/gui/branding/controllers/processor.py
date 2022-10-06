from gui import SystemMessages
from .._constants import UI_TYPE
from ..data import g_dataHolder
from ..lang import l10n
from vehicle_outfit.outfit import Outfit
from items.components.c11n_constants import ApplyArea
from items.customizations import CustomizationOutfit, CamouflageComponent, DecalComponent

__all__ = ('ProcessorController', )

class ProcessorController(object):

	@staticmethod
	def findPresetByID(presetID):
		for preset in g_dataHolder.config['presets']:
			if preset['id'] == presetID:
				return preset
		return None

	@staticmethod
	def getOutfit(originalOutfit, preset, vDesc):

		camouflages, decals, paints = [], [], []
		hullSlotsNum, turretSlotsNum = 0, 0

		for emblemSlot in vDesc.hull.emblemSlots:
			if emblemSlot.type == 'inscription':
				hullSlotsNum += 1
		for emblemSlot in vDesc.turret.emblemSlots:
			if emblemSlot.type == 'inscription':
				turretSlotsNum += 1

		paintID = preset.get('paint', 0)
		cammoCompID = preset['camouflage']
		logoCompID = preset['logotype']
		advertCompID1, advertCompID2 = preset['advert']
		storedSoloSlot = False

		if cammoCompID == 0 and logoCompID == 0 and advertCompID1 == 0 and advertCompID2 == 0:
			return originalOutfit

		if cammoCompID > 0:
			camouflages.append(CamouflageComponent(id=cammoCompID, appliedTo=ApplyArea.HULL))
			camouflages.append(CamouflageComponent(id=cammoCompID, appliedTo=ApplyArea.TURRET))
			camouflages.append(CamouflageComponent(id=cammoCompID, appliedTo=ApplyArea.GUN))

		if logoCompID > 0:
			decals.append(DecalComponent(id=logoCompID, appliedTo=ApplyArea.HULL))
			decals.append(DecalComponent(id=logoCompID, appliedTo=ApplyArea.HULL_1))
			decals.append(DecalComponent(id=logoCompID, appliedTo=ApplyArea.TURRET))
			decals.append(DecalComponent(id=logoCompID, appliedTo=ApplyArea.TURRET_1))
			decals.append(DecalComponent(id=logoCompID, appliedTo=ApplyArea.GUN))
			decals.append(DecalComponent(id=logoCompID, appliedTo=ApplyArea.GUN_1))

		if advertCompID1 > 0:
			if hullSlotsNum == 1 and turretSlotsNum == 1:
				decals.append(DecalComponent(id=advertCompID1, appliedTo=ApplyArea.HULL_2))
				decals.append(DecalComponent(id=advertCompID1, appliedTo=ApplyArea.HULL_3))
			elif hullSlotsNum == 2:
				decals.append(DecalComponent(id=advertCompID1, appliedTo=ApplyArea.HULL_2))
			elif turretSlotsNum == 2:
				decals.append(DecalComponent(id=advertCompID1, appliedTo=ApplyArea.TURRET_2))
				decals.append(DecalComponent(id=advertCompID1, appliedTo=ApplyArea.GUN_2))
			elif hullSlotsNum + turretSlotsNum == 1:
				decals.append(DecalComponent(id=advertCompID1, appliedTo=ApplyArea.HULL_2))
				decals.append(DecalComponent(id=advertCompID1, appliedTo=ApplyArea.HULL_3))
				storedSoloSlot = True

		if advertCompID2 > 0:
			if hullSlotsNum == 1 and turretSlotsNum == 1:
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.TURRET_2))
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.GUN_2))
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.TURRET_3))
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.GUN_3))
			elif hullSlotsNum == 2:
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.HULL_3))
			elif turretSlotsNum == 2:
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.TURRET_3))
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.GUN_3))
			elif hullSlotsNum + turretSlotsNum == 1 and not storedSoloSlot:
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.HULL_2))
				decals.append(DecalComponent(id=advertCompID2, appliedTo=ApplyArea.HULL_3))

		if paintID > 0:
			paints.append(DecalComponent(id=paintID, appliedTo=ApplyArea.CHASSIS))
			paints.append(DecalComponent(id=paintID, appliedTo=ApplyArea.GUN))
			paints.append(DecalComponent(id=paintID, appliedTo=ApplyArea.GUN_2))

		customizationOutfit = CustomizationOutfit(camouflages=camouflages, decals=decals, paints=paints)
		return Outfit(customizationOutfit.makeCompDescr())

	def appendSettings(self, ctx):
		g_dataHolder.cache['currentSetup'] = [int(ctx['teamFirst']), int(ctx['teamSecond'])]
		g_dataHolder.cache['onlyOnMyTank'] = ctx['onlyOnMyTank']
		if g_dataHolder.config['UIType'] == UI_TYPE.OPERATOR:
			self.__pushSystemMessageOperator()
		elif g_dataHolder.config['UIType'] == UI_TYPE.PLAYER:
			self.__pushSystemMessagePlayer()

	def __pushSystemMessageOperator(self):
		preset1 = self.findPresetByID(g_dataHolder.cache['currentSetup'][0])
		name1 = preset1['name'] if preset1 else "Unknown"
		preset2 = self.findPresetByID(g_dataHolder.cache['currentSetup'][1])
		name2 = preset2['name'] if preset2 else "Unknown"
		message = l10n('ui.operator.messageTeams').format(name1=name1, name2=name2)
		SystemMessages.pushMessage(message, type=SystemMessages.SM_TYPE.Warning)

	def __pushSystemMessagePlayer(self):
		if g_dataHolder.cache['onlyOnMyTank']:
			preset = self.findPresetByID(g_dataHolder.cache['currentSetup'][0])
			name = preset['name'] if preset else "Unknown"
			message = l10n('ui.player.messageOwnTank').format(name=name)
			SystemMessages.pushMessage(message, type=SystemMessages.SM_TYPE.Warning)
		else:
			preset1 = self.findPresetByID(g_dataHolder.cache['currentSetup'][0])
			name1 = preset1['name'] if preset1 else "Unknown"
			preset2 = self.findPresetByID(g_dataHolder.cache['currentSetup'][1])
			name2 = preset2['name'] if preset2 else "Unknown"
			message = l10n('ui.player.messageTeams').format(name1=name1, name2=name2)
			SystemMessages.pushMessage(message, type=SystemMessages.SM_TYPE.Warning)
