// https://stackoverflow.com/a/9188211
// Converts player dict to array and sorts by position
// TODO handle putting current player last
export default function sortPlayers(playersDict){
    let playersArray = Object.values(playersDict);
    playersArray.sort(function(a, b){
      return a.position < b.position ? 1 : -1
    });
    return playersArray
}

// modules.exports.sortPlayers = sortPlayers;