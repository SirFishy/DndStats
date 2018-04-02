from app.dndstats import db
from sqlalchemy import ForeignKey
import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    characters = db.relationship('PlayerCharacter', backref='player', lazy='dynamic')
    campaigns = db.relationship('Campaign', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    campaignname = db.Column(db.String(64), index=True, unique=True)
    dungeonmaster = db.Column(db.Integer, db.ForeignKey('user.id'))
    players = db.relationship('User', backref='players', lazy='dynamic')
    playercharacters = db.relationship('PlayerCharacter', backref='characters', lazy='dynamic')
    stats = db.relationship('Stat', backref='stat', lazy='dynamic')

    def __repr__(self):
        return '<Campaign {}>'.format(self.campaignname)


class PlayerCharacter(db.Model):
    __tablename__ = 'playercharacter'
    id = db.Column(db.Integer, primary_key=True)
    charactername = db.Column(db.String(64), index=True, unique=True)
    stats = db.relationship('Stat', backref='accolade', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))

    def __repr__(self):
        return '<PC {}>'.format(self.charactername)


class Weapon(db.Model):
    __tablename__ = 'weapon'
    id = db.Column(db.Integer, primary_key=True)
    weaponname = db.Column(db.String(64), index=True, unique=True, primary_key=True)

    def __repr__(self):
        return '<Weapon Name{}>'.format(self.weaponname)


class Spell(db.Model):
    __tablename__ = 'spell'
    id = db.Column(db.Integer, primary_key=True)
    spellname = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    spelllevel = db.Column(db.Integer(), index=True)

    def __repr__(self):
        return '<Spell Name{}, DisplayName{}>'.format(self.npcname, self.displayname)


class NPC(db.Model):
    __tablename__ = 'npc'
    id = db.Column(db.Integer, primary_key=True)
    npcname = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    displayname = db.Column(db.String(64), index=True)
    imageurl = db.Column(db.String(128))

    def __repr__(self):
        return '<NPC Name{}, DisplayName{}>'.format(self.npcname, self.displayname)


class AttackType(db.Model):
    __tablename__ = 'attacktype'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))

    def __repr__(self):
        return '<AttackType Name{}>'.format(self.weaponname)

    __mapper_args__ = {
        'polymorphic_identity': 'attacktype',
        'polymorphic_on': type,
        'with_polymorphic': '*'
    }


class WeaponAttack(db.Model):
    __tablename__ = 'weaponattack'
    id = db.Column(db.Integer, ForeignKey('attacktype.id'), primary_key=True)
    weapon_id = db.Column(db.Integer, ForeignKey('weapon.id'))

    def __repr__(self):
        return '<WeaponAttack Weapon{}>'.format(self.weapon_id)

    __mapper_args__ = {
        'polymorphic_identity': 'weaponattack',
        'polymorphic_load': 'inline'
    }


class SpellAttack(db.Model):
    __tablename__ = 'spellattack'
    id = db.Column(db.Integer, ForeignKey('attacktype.id'), primary_key=True)
    spell_id = db.Column(db.Integer, ForeignKey('spell.id'))

    def __repr__(self):
        return '<SpellAttack Spell{}>'.format(self.spell_id)

    __mapper_args__ = {
        'polymorphic_identity': 'spellattack',
        'polymorphic_load': 'inline'
    }


class Stat(db.Model):
    __tablename__ = 'stat'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())
    session = db.Column(db.Integer, index=True)
    type = db.Column(db.String(64))
    playercharacter_id = db.Column(db.Integer, db.ForeignKey('playercharacter.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))

    def __repr__(self):
        return '<Stat Datetime{}, session{}>'.format(self.timestamp, self.session)

    __mapper_args__ = {
        'polymorphic_identity':'stat',
        'polymorphic_on':type,
        'with_polymorphic': '*'
    }


class Hit(db.Model):
    __tablename__ = 'hit'
    id = db.Column(db.Integer, ForeignKey('stat.id'), primary_key=True)
    npc_id = db.Column(db.Integer, db.ForeignKey('npc.id'))
    attacktype_id = db.Column(db.Integer, db.ForeignKey('attacktype.id'))
    damage = db.Column(db.Integer(), index=True)

    def __repr__(self):
        return '<Hit NPC{}, Damage{}>'.format(self.npc_id, self.damage)

    __mapper_args__ = {
        'polymorphic_identity':'hit',
        'polymorphic_load': 'inline'
    }


class Miss(db.Model):
    __tablename__ = 'miss'
    id = db.Column(db.Integer, ForeignKey('stat.id'), primary_key=True)
    npc_id = db.Column(db.Integer, db.ForeignKey('npc.id'))
    attacktype_id = db.Column(db.Integer, db.ForeignKey('attacktype.id'))

    def __repr__(self):
        return '<Miss NPC{}>'.format(self.npc_id)

    __mapper_args__ = {
        'polymorphic_identity':'miss',
        'polymorphic_load': 'inline'
    }


class NPCKilled(db.Model):
    __tablename__ = 'npckilled'
    id = db.Column(db.Integer, ForeignKey('stat.id'), primary_key=True)
    npc_id = db.Column(db.Integer, db.ForeignKey('npc.id'))
    description = db.Column(db.String(500))

    def __repr__(self):
        return '<Stat NPC{}, Description{}>'.format(self.npc_id, self.description)

    __mapper_args__ = {
        'polymorphic_identity':'npckilled',
        'polymorphic_load': 'inline'
    }


class SpellUsed(db.Model):
    __tablename__ = 'spellused'
    id = db.Column(db.Integer, ForeignKey('stat.id'), primary_key=True)
    spell_id = db.Column(db.Integer, ForeignKey('spell.id'))
    description = db.Column(db.String(500))

    def __repr__(self):
        return '<Stat Spell{}, Description{}>'.format(self.spell_id, self.description)

    __mapper_args__ = {
        'polymorphic_identity':'spellused',
        'polymorphic_load': 'inline'
    }
