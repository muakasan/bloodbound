const Team = {
  RED: "red",
  BLUE: "blue",
};

const Token = {
  GREY: "grey",
  BLUE: "blue",
  RED: "red",
  RANK: "rank",
};

const Role = {
  ELDER: 1,
  ASSASSIN: 2,
  HARLEQUIN: 3,
  ALCHEMIST: 4,
  MENTALIST: 5,
  GUARDIAN: 6,
  BERSERKER: 7,
  MAGE: 8,
  COURTESAN: 9,
};

const RoleToStr = {
  1: "elder",
  2: "assassin",
  3: "harlequin",
  4: "alchemist",
  5: "mentalist",
  6: "guardian",
  7: "beserker",
  8: "mage",
  9: "courtesan",
}

const Item = {
  SWORD: "sword",
  FAN: "fan",
  STAFF: "staff",
  SHIELD: "shield",
  QUILL: "quill",
  TRUECURSE: "truecurse",
  FALSECURSE: "falsecurse",
};

const Step = {
  LOBBY: "lobby",
  INGAME: "ingame",
  COMPLETE: "complete",
};

export { Token, Role, Item, Step, RoleToStr };
