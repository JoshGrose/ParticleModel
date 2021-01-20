//filepaths !!!!!!!!!!!!!!
var curr_dir = "//work//07329//joshg//stampede2//simulations//ParticleModel//results_mod//particle_FULLset4_4000_newbed"
var filepath = curr_dir // '//work//07329//joshg//stampede2//simulations//ParticleModel//results//particle_FULLset4_4_newbed//';		                // location of parts (nanoparticles)
var file_in_1 = curr_dir.concat("//air_pieces.txt")  // "//work//07329//joshg//stampede2//simulations//ParticleModel//results//particle_FULLset4_400_newbed//aair_pieces.txt"
var file_in_2 = curr_dir.concat("//part_num.txt")  // curr_dir + "//part_num.txt" // "//work//07329//joshg//stampede2//simulations//ParticleModel//results//particle_FULLset4_4_newbed//part_num.txt";  //"W:\\text_0\\part_num.txt";		      									// location of this file (number of particles in system)

var ForReading = 1;

// import conversion information=n (number of parts)    
fso = new ActiveXObject("Scripting.FileSystemObject");
//ado = new ActiveXObject("ADODB.Stream");
ts = fso.OpenTextFile(file_in_1, ForReading, true);
//ball = ts[1];  
var s = ts.ReadLine();
var air_pieces = s; //.toString();
ts.Close();

fso2 = new ActiveXObject("Scripting.FileSystemObject");
//ado = new ActiveXObject("ADODB.Stream");
ts2 = fso2.OpenTextFile(file_in_2, ForReading, true);
//ball = ts[1]; 
var s2 = ts2.ReadLine();
var part_num = s2; //.toString();
ts2.Close();

// import file 
var BodyNameArray = [];
var air_string = filepath.concat("//AirBlock.step")
var imp1=ag.b.Import(air_string); 
imp1.Name= "AirBlock";

for (var i = 0; i < air_pieces; i++) {
    BodyNameArray = BodyNameArray.concat(imp1.Name);
}

//Create and implement slicing plane
//BodyNameArray = BodyNameArray.concat(imp1.Name);

// Take the YZ Plane
//var plyz = agb.GetYZPlane();

//var plane = agb.PlaneFromPlane(plyz);  // take this Type

//plane.Name = "Slice_Plane"; // Name the new planes
//plane.AddTransform(agc.XformZOffset, .0005145); // .000549// Give an X-offset to the new planes -- probably should also grab this from a text file
//agb.SetActivePlane(plane);
//var feature = ag.gui.CreateSlice(); // added .b.
//ag.gui.Commit(); // added .b.
//feature.PutBasePlane(plane);
//ag.gui.Regen(); // added .b.

// reset plane
//var plxy = agb.GetXYPlane();
//agb.SetActivePlane(plxy);

var air_string_ext = filepath.concat("//AirBlockExt.step")
var imp1=ag.b.Import(air_string_ext); 
imp1.Name="AirBlock2";
BodyNameArray = BodyNameArray.concat("AirBlock");

pCount = 0;
var StepNamesArray = [];
var StepFilesArray = [];
var NumArray = [];

for (var i = 0; i < part_num; i++) {
    var part = i+1;
	NumArray = NumArray.concat(part.toString())
}

// var NumArray = ['1','2','3','4','5'] //['19','20','21','22','23'] //['58', '44', '61', '93', '92', '95','96', '94', '97', '98', '99', '100', '101', '102', '103', '104', '91'];
var numArrayLength = NumArray.length;
var particle_filename = filepath.concat('//Particle');
for (var i = 0; i < numArrayLength; i++) {
    pCount = pCount +1;
    StepFilesArray = StepFilesArray.concat(particle_filename.concat(NumArray[i], '.step'))
    StepNamesArray = StepNamesArray.concat('Particle'.concat(NumArray[i]))
    BodyNameArray = BodyNameArray.concat('Particle '.concat(pCount.toString()))
}

var NumArray2 = [];
var NumArrayTot = NumArray.concat(NumArray2);
var arrayLength = StepFilesArray.length;
for (var i = 0; i < arrayLength; i++) {
    var imp1=ag.b.Import(StepFilesArray[i]);  // IAnsImport
    imp1.Name= "Particle_".concat(NumArrayTot[i]);
}

var glass_string = filepath.concat("//glass_block.step")
var imp1=ag.b.Import(glass_string);  // IAnsImport
imp1.Name="GlassBlock";
BodyNameArray = BodyNameArray.concat(imp1.Name)

// import bubble mesh bubble BOI
var bubble_string = filepath.concat("//bubble.stp");
var imp1=ag.b.Import(bubble_string);
imp1.Name= "bubble";
BodyNameArray = BodyNameArray.concat(imp1.Name);

//rename for mechanical
ag.gui.Regen();

for (var i = 0; i < ag.fm.BodyCount; i++)
{      
    var f1=ag.fm.body(i);
    f1.Name = BodyNameArray[i]; //BodyNameArray[i];
}

ag.gui.Regen();
