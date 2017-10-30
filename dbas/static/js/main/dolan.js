/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function dolan_translate(dictionary, inputText) {
    'use strict';
    
    var translatedText;
    var replacement;
    var regex;

    translatedText = inputText;

    $.each(dictionary, function(key, value){
        replacement = dictionary[key][Math.floor(Math.random() * dictionary[key].length)];
        regex = new RegExp("\\b("+key+")\\b", 'gi');
        translatedText = translatedText.replace(regex, replacement);
    });
        
    return translatedText;
}

var dolan_dictionary = {
    "about":               ["abt", "abot"],
    "above":               ["aboev"],
    "accept":              ["acept"],
    "actually":            ["accualy", "acuali", "accually"],
    "addicted":            ["adikted"],
    "addict":              ["adikt"],
    "after":               ["aftr"],
    "again":               ["egen", "agen"],
    "all":                 ["al"],
    "allergic":            ["allergicc"],
    "america":             ["amerika"],
    "anal":                ["anl"],
    "and":                 ["nd", "n"],
    "anger":               ["angr", "angrey"],
    "animal":              ["animel"],
    "anniversary":         ["anibersary"],
    "anus":                ["anis"],
    "april":               ["aprel"],
    "are":                 ["r", "ar"],
    "ashley":              ["sexai bish"],
    "avengers":            ["avengars"],
    "awesome":             ["awsum"],
    "argumentation":       ["agrumentatin"],
    "bacon":               ["bacons"],
    "bail":                ["belz"],
    "bastard":             ["besterd"],
    "bat":                 ["btat"],
    "batman":              ["btmn"],
    "beautiful":           ["baetuiful"],
    "because":             ["cuz", "bcuz", "bcus"],
    "bed":                 ["bedd"],
    "beer":                ["bier"],
    "before":              ["befo", "bfur", "befur", "bfare", "bfor"],
    "better":              ["beter", "beder"],
    "birth":               ["birt", "brth"],
    "birthday":            ["byrthdayz", "burfdy", "birfday"],
    "bitch":               ["betch"],
    "block":               ["blok"],
    "blocked":             ["blokd"],
    "black":               ["bleck", "blaek"],
    "blood":               ["blud"],
    "blow":                ["blw"],
    "bobman":              ["bbmen"],
    "boobs":               ["bewbz"],
    "both":                ["boas"],
    "boys":                ["bois"],
    "brain":               ["brean"],
    "brick":               ["brik"],
    "bro":                 ["bor"],
    "bugs":                ["bogs"],
    "broken":              ["boerkn"],
    "brother":             ["brotr", "brthr"],
    "bucks":               ["bukz"],
    "builder":             ["buildr", "bulder"],
    "bumholes":            ["bumholez"],
    "business":            ["businss", "biznus"],
    "busy":                ["busi"],
    "buttsex":             ["bhutt secks"],
    "based":               ["buhsed"],
    "cake":                ["kake"],
    "can":                 ["caen"],
    "cancer":              ["cansor", "cansur"],
    "candle":              ["cnadl", "candel"],
    "cant":                ["ctan"],
    "can't":               ["ca'nt", "cant", "ctan"],
    "care":                ["caret"],
    "carrot":              ["karot"],
    "cash":                ["kash"],
    "cat":                 ["kat"],
    "cause":               ["cuz"],
    "center":              ["centar"],
    "change":              ["chanj"],
    "checkup":             ["chekup"],
    "chicken":             ["chikn"],
    "chill pill":          ["chilpil"],
    "chill pills":         ["chilpils"],
    "chocolade":           ["chocolat"],
    "chrome":              ["cohrme"],
    "chuck":               ["chak"],
    "cigarette":           ["cigrete"],
    "clear":               ["clier"],
    "clown":               ["clauwn"],
    "come on":             ["cum on"],
    "come":                ["coem"],
    "contact":             ["cuntact"],
    "conspiracy":          ["cnspaercy"],
    "contex":              ["cntex"],
    "cooking":             ["cuking"],
    "copyright":           ["copyrites"],
    "couch":               ["cuch"],
    "could":               ["cud"],
    "crash":               ["crehs"],
    "created":             ["crated"],
    "crying":              ["criyin"],
    "cupcake":             ["cupcaek"],
    "cupcakes":            ["cupcaeks"],
    "cute":                ["cuet"],
    "dammit":              ["demmit"],
    "damn":                ["dayum", "demn"],
    "date":                ["dayte", "dait"],
    "dead":                ["ded"],
    "demo":                ["dehmu"],
	"D-BAS":               ["DaBaS_minus"],
    "delicious":           ["dlishus"],
    "die":                 ["dei", "dy"],
    "dinner":              ["dinnr", "dner"],
    "discussion":          ["diskazzn"],
    "discussions":         ["diskazznz"],
    "disney":              ["dosni"],
    "divide":              ["deviding"],
    "do":                  ["dew", "do"],
    "doctor":              ["docte"],
    "doesn't":             ["dsnt"],
    "dollar":              ["dolar"],
    "dollars":             ["dolars"],
    "don't know":          ["dunno"],
    "don't":               ["dunt", "doent", "dnot"],
    "donald":              ["dolan"],
    "double":              ["duble"],
    "dream":               ["drem"],
    "drinking":            ["drinkig"],
    "drunk":               ["dronk"],
    "dialog":              ["dualig"],
    "easy":                ["esi"],
    "egg":                 ["eg"],
    "eggs":                ["egs"],
    "eleven":              ["elven"],
    "enjoy":               ["enjoi", "njoi"],
    "entire":              ["entrire"],
    "ever":                ["evur", "evir"],
    "every time":          ["evrytim"],
    "everyone":            ["evryon"],
    "every thing":         ["evryting", "everiting", "everyting"],
    "everything":          ["evryting", "everiting", "everyting"],
    "everytime":           ["evrytim"],
    "examination":         ["examnashun"],
    "evil":                ["evul", "evel"],
    "exist":               ["exeest"],
    "eyeballs":            ["eyebals"],
    "eyes":                ["eeys"],
    "faggot":              ["feget", "faggat", "fgt"],
    "famous":              ["famus"],
    "feedback":            ["fidbuck"],
    "finally":             ["finully"],
    "finger":              ["fingor"],
    "fire":                ["fier"],
    "floor":               ["flour", "flur"],
    "flower":              ["flowa"],
    "fools":               ["fules"],
    "for":                 ["fer","fur", "four", "4"],
    "forgot":              ["frogot"],
    "friend":              ["frend", "flend"],
    "from":                ["frem"],
    "fuck":                ["fak", "faq", "fk", "fek", "feq", "fuk", "fck"],
    "fucking":             ["fakn", "fakin", "fukin", "fukn"],
    "funny":               ["funey", "fany", "funnay"],
    "game":                ["gaem", "gaym"],
    "garden":              ["gurden"],
    "gasoline":            ["gaseline"],
    "gay":                 ["gya"],
    "gee":                 ["g"],
    "gentlemen":           ["gntelmen"],
    "get":                 ["git", "get"],
    "girlfriend":          ["grilfrend"],
    "glory":               ["glroy"],
    "god":                 ["gawd"],
    "godbrother":          ["gdbrthr"],
    "golf":                ["gorf"],
    "going to":            ["gunna", "gona"],
    "gonna":               ["gunna", "gona"],
    "good":                ["gud"],
    "goofy":               ["gooby"],
    "got":                 ["gawt"],
    "guess":               ["gess"],
    "guy":                 ["gui", "guy"],
    "guys":                ["guise"],
    "hand":                ["hamd"],
    "happened":            ["hapnd"],
    "happening":           ["hapenin"],
    "happiest":            ["hapiest"],
    "happy":               ["hapy", "hapy"],
    "hate":                ["haet"],
    "hating":              ["heatin"],
    "have":                ["has", "haz", "haev", "heiv", "hav"],
    "haven't":             ["havn"],
    "he":                  ["hi"],
    "heart":               ["hert"],
    "hello":               ["hlelo"],
    "help":                ["halp"],
    "here":                ["heer", "hur"],
    "high":                ["hi"],
    "hijack":              ["hijak"],
    "hipster":             ["hpistr"],
    "host":                ["hosd"],
    "how":                 ["how", "hw"],
    "i":                   ["ei", "i", "ai"],
    "i'm":                 ["im"],
    "i am":                ["im"],
    "idea":                ["idia"],
    "idgaf":               ["igaf"],
    "idiot":               ["idoit", "edeot", "ideot"],
    "idk":                 ["kdi"],
    "in a car":            ["incar"],
    "in":                  ["n"],
    "inception":           ["inceptyon"],
    "is":                  ["es", "iz"],
    "islam":               ["izlam"],
    "it":                  ["et"],
    "jesus":               ["jizzus", "jzuz"],
    "jewelry":             ["jewlry"],
    "juice":               ["jewce"],
    "juicy":               ["joocy"],
    "just":                ["juts"],
    "karagon":             ["karafap", "kragon"],
    "keep":                ["keip", "kepe"],
    "kids":                ["keds"],
    "kill":                ["kel", "kil"],
    "kingdom":             ["kendum"],
    "krauthoff":           ["Dolan"],
    "knwo":                ["kno"],
    "language":            ["lungage"],
    "later":               ["laytor"],
    "let's":               ["lest", "les", "lez"],
    "life":                ["lif", "liyfe", "lyfe"],
    "like":                ["leik", "lyk", "lik", "liek"],
    "linkin park":         ["link park"],
    "lisa":                ["lis"],
    "live":                ["liv"],
    "lol":                 ["lul"],
    "long":                ["lnog"],
    "look":                ["luk", "lok"],
    "looks":               ["loks", "luks"],
    "lost":                ["losd"],
    "love":                ["luv"],
    "make":                ["maek", "mak"],
    "married":             ["marreyd"],
    "masterbate":          ["fap"],
    "matter":              ["maddr"],
    "may":                 ["mey"],
    "mcdonalds":           ["mcdolanz"],
    "me":                  ["meh"],
    "meanwhile":           ["maenwihle"],
    "medicine":            ["medsin"],
    "metal":               ["mteal"],
    "mexican":             ["border jumper"],
    "minecraft":           ["minkreft"],
    "minute":              ["minit", "minut"],
    "modern":              ["modurn"],
    "modernest":           ["modurnest"],
    "moment":              ["momunt"],
    "mona":                ["muna"],
    "mister":              ["mistur"],
    "ministry":            ["minstri"],
    "monster":             ["menstr"],
    "monthly":             ["monfly"],
    "moralfag":            ["morelfeg", "mrlfeg"],
    "more":                ["mor", "moar"],
    "motherfucker":        ["motrfukr", "motrfuker", "motrfakr", "motrfaker", "mtherfukr", "mtherfuker", "mtherfakr", "mtherfaker"],
    "mr":                  ["mistur"],
    "muscles":             ["msucels"],
    "muslim":              ["mozlem"],
    "must":                ["mus"],
    "my":                  ["mai", "mi", "mah"],
    "nature":              ["nateur"],
    "nazi":                ["natzi"],
    "need":                ["nede", "ned"],
    "never":               ["neer"],
    "new":                 ["nue "],
    "nice":                ["niec"],
    "nigger":              ["nigur", "niger"],
    "niggers":             ["nigurs", "nigers", "nigges"],
    "not":                 ["not", "no"],
    "nothing":             ["nuthng"],
    "now":                 ["nao", "naw", "naow", "nw"],
    "number":              ["nmber"],
    "news":                ["nwhs"],
    "obama":               ["negropres", "obama"],
    "of":                  ["of", "uv", "ef"],
    "ok":                  ["k"],
    "okay":                ["k"],
    "other":               ["ohtr"],
    "outside":             ["outsed"],
    "online":              ["ohnlene"],
    "page":                ["paeg"],
    "party":               ["paryt"],
    "pass":                ["pas"],
    "participation":       ["partipotian"],
    "peanuts":             ["peenutz"],
    "people":              ["ppl"],
    "pick":                ["pik"],
    "picture":             ["pishur"],
    "planet":              ["planut"],
    "play":                ["pley", "pray"],
    "please":              ["pls", "plss", "plz", "plx"],
    "plox":                ["plx"],
    "pluto":               ["pruto"],
    "police":              ["poleec"],
    "por favor":           ["prf avor"],
    "power":               ["pwoer"],
    "pretty":              ["prety"],
    "production":          ["prodization"],
    "quick":               ["quik"],
    "quickest":            ["qiukest"],
    "rage":                ["raeg"],
    "rainbow dash":        ["arnbo"],
    "rape":                ["raep", "reap"],
    "raped":               ["raeped", "reaped", "raepd", "reapd"],
    "rarity":              ["rarty"],
    "read":                ["raed", "red"],
    "real":                ["reel"],
    "really":              ["rly", "relly", "rely"],
    "rest":                ["rast"],
    "research":            ["rasurch"],
    "report":              ["ripurt"],
    "rick roll":           ["rix role"],
    "ride":                ["ried", "ryde"],
    "rocks":               ["racks"],
    "said":                ["sayd", "sed"],
    "satan":               ["saytan"],
    "say":                 ["sya"],
    "scared":              ["scraed"],
    "scooby":              ["skubby"],
    "seat":                ["seet"],
    "second":              ["sec"],
    "secret":              ["sicret"],
    "see":                 ["c"],
    "seeing":              ["seein"],
    "send":                ["snd", "sen"],
    "service":             ["srvize", "sorvize"],
    "sex":                 ["sehx", "seks"],
    "sexy":                ["seyx"],
    "shall":               ["shell"],
    "share":               ["shar"],
    "shirt":               ["sirht"],
    "shit":                ["shet", "shyt"],
    "shop":                ["shopn"],
    "show":                ["shwo"],
    "shower":              ["showr"],
    "sick":                ["sik"],
    "skiing":              ["skeeing"],
    "skrillex":            ["skrix", "skrlx"],
    "sleep":               ["slep"],
    "smd":                 ["smpcb"],
    "smile":               ["smiel"],
    "sniper":              ["sniepr"],
    "some":                ["soem", "sum"],
    "somebody":            ["soembady", "sumbudy", "sumbody", "sumbdy"],
    "someone":             ["sum1"],
    "something":           ["sumthn", "smthn", "somseng"],
    "sorry":               ["sawry"],
    "spiderman":           ["spooderman", "spodermn", "spoodermin", "spoodey", "spody"],
    "stay":                ["sty"],
    "steak":               ["stek"],
    "stop":                ["stup", "stap", "stahp"],
    "story":               ["stori"],
    "stranger":            ["strngr"],
    "structure":           ["stracta"],
    "stuck":               ["sutck"],
    "stupid":              ["stopid", "stuped", "stupd"],
    "style":               ["styel"],
    "suck":                ["suk", "sak", "sk", "saq", "seq", "sek"],
    "sucking":             ["sukn", "sakin", "sukin"],
    "suitcase":            ["sootcais"],
    "sup":                 ["sap"],
    "super":               ["spuer"],
    "system":              ["sustem"],
    "sure":                ["shor", "shur", "shure", "suer"],
    "take":                ["taek", "tak"],
    "taste":               ["tast", "taest"],
    "teacher":             ["taechr"],
    "tell":                ["tael"],
    "terrorist":           ["teroras"],
    "testa":               ["tsta"],
    "than":                ["thans"],
    "thank you":           ["ty"],
    "thanks":              ["tanks", "ty"],
    "that":                ["dat"],
    "the":                 ["teh", "da"],
    "them":                ["dem"],
    "then":                ["ten"],
    "therapist":           ["theerpist"],
    "therapy":             ["thrapy"],
    "there":               ["ther"],
    "they":                ["dey"],
    "thing":               ["thinng"],
    "this":                ["dis", "tis"],
    "though":              ["tuff"],
    "till":                ["til"],
    "time":                ["tiem"],
    "times":               ["tiems"],
    "titties":             ["tittays"],
    "to":                  ["too", "2", "tu", "t", "tew"],
    "toaster":             ["toastre"],
    "today":               ["todei"],
    "too":                 ["too", "2", "tu", "t", "tew"],
    "trade":               ["traed"],
    "trick":               ["trik"],
    "trolled":             ["troled", "trold", "trolde"],
    "truck":               ["turk"],
    "true":                ["tru", "trew"],
    "trying":              ["trieng"],
    "tsunami":             ["tusnami"],
    "tsunamis":            ["tusnamis"],
    "turn":                ["tern"],
    "twilight":            ["twalot"],
    "type":                ["tiep"],
    "ultimate":            ["ultimaet"],
    "uncle":               ["uncel", "unecl"],
    "until":               ["til"],
    "unexpected":          ["unepecxted"],
    "unproffesional":      ["unprofeshnl"],
    "venom":               ["venam"],
    "very":                ["vury"],
    "virgin":              ["vargin"],
    "virginity":           ["vnrginty"],
    "wait":                ["waet", "wate", "wayt"],
    "wallpaper":           ["walpeeper", "walpapr"],
    "walt":                ["wolt"],
    "wanna":               ["wan"],
    "want":                ["wnt", "wnta", "wan"],
    "was":                 ["wuz"],
    "wash":                ["waesh"],
    "watch":               ["wacht", "wacth"],
    "water":               ["woter", "wtr"],
    "we are":              ["we"],
    "we're":               ["we"],
    "wearing":             ["weerin"],
    "website":             ["websyt"],
    "well":                ["wlel", "wull"],
    "went":                ["wnt"],
    "welcome":             ["welkohme"],
    "what would dolan do": ["what would dolan does"],
    "what":                ["wat", "wot"],
    "what's up":           ["sup"],
    "whatever":            ["watevur"],
    "why":                 ["wai", "y", "wy"],
    "will":                ["wil"],
    "windows":             ["windos"],
    "with":                ["wit", "wiv"],
    "without":             ["weetout"],
    "wizard":              ["wizerd"],
    "women":               ["wmen"],
    "woof":                ["arf"],
    "work":                ["wrok"],
    "world":               ["wrld", "wurld", "wolrd"],
    "would":               ["wud", "wuld"],
    "wrong":               ["rong"],
    "year":                ["yr", "yaer"],
    "years":               ["yrs", "yaers"],
    "york":                ["yirk"],
    "you":                 ["you", "u", "yuo", "yu", "yuu"],
    "your":                ["ur", "yer", "yur", "yor"],
    "yourself":            ["yurselv"],
    "school":              ["skewl"]

};