/*
    Author: Jonathan Lurie - http://me.jonathanlurie.fr
    License: MIT
    
    The point of this little gist is to fix the issue of losing
    typed arrays when calling the default JSON serilization.
    The default mode has for effect to convert typed arrays into
    object like that: {0: 0.1, 1: 0.2, 2: 0.3} what used to be
    Float32Array([0.1, 0.2, 0.3]) and once it takes the shape of an
    object, there is no way to get it back in an automated way!
    
    The fix leverages the usually-forgotten functions that can be
    called as arguments of JSON.stringify and JSON.parse: the
    replacer and the reviver.
*/

// get the glogal context for compatibility with node and browser
var context = typeof window === "undefined" ? global : window;

// flag that will be sliped in the json string
const FLAG_TYPED_ARRAY = "FLAG_TYPED_ARRAY";

// an object that contains a typed array, among other things
var obj = {
  bli: "blibli",
  bla: new Float32Array([10, 20, 30, 40]),
  blou: {
    blouFoo: 23,
    blouFii: new Uint8Array([100, 200, 300, 400]),
    blouFuu: "lklklkl"
  }
}

console.log("---------------------");
console.log('The original object:');
console.log( obj );

// ENCODING ***************************************

var jsonStr = JSON.stringify( obj , function( key, value ){
  // the replacer function is looking for some typed arrays.
  // If found, it replaces it by a trio
  if ( value instanceof Int8Array         ||
       value instanceof Uint8Array        ||
       value instanceof Uint8ClampedArray ||
       value instanceof Int16Array        || 
       value instanceof Uint16Array       ||
       value instanceof Int32Array        || 
       value instanceof Uint32Array       || 
       value instanceof Float32Array      ||
       value instanceof Float64Array       )
  {
    var replacement = {
      constructor: value.constructor.name,
      data: Array.apply([], value),
      flag: FLAG_TYPED_ARRAY
    }
    return replacement;
  }
  return value;
});

console.log("---------------------");
console.log('The JSON string, look at this sneaky replacement!');
console.log( jsonStr );

// DECODING ***************************************


var decodedJson = JSON.parse( jsonStr, function( key, value ){
  // the reviver function looks for the typed array flag
  try{
    if( "flag" in value && value.flag === FLAG_TYPED_ARRAY){
      // if found, we convert it back to a typed array
      return new context[ value.constructor ]( value.data );
    }
  }catch(e){}
  
  // if flag not found no conversion is done
  return value;
});

console.log("---------------------");
console.log('Supposedly the same as the original object:');
console.log( decodedJson );

/*
    Of course if you do that to store your data in a file, it can be convenient.
    BUT, if your typed arrays are quite large, (few thousands figures in total) considere two things:
      - the json serialization is limited in number of characters
      - typed array play well with file buffer, use that instead!
*/