// filepath strings !!!!!!!!!!!
var curr_dir = "//work//07329//joshg//stampede2//simulations//ParticleModel//results_mod//particle_FULLset4_4000_newbed"
var filepath = curr_dir // '//work//07329//joshg//stampede2//simulations//ParticleModel//ansys_scripts//NanoparticleOutput//Results4//';         // wherever you want the temperature results to go (same as wbpj output filepath)
var file_string = curr_dir // "//work//07329//joshg//stampede2//simulations//ParticleModel//results//particle_FULLset4_4_newbed//";
var file_in = file_string.concat("//part_bound.txt");                        // wherever this file is located

// import data from text file
var ForReading = 1;
fso = new ActiveXObject("Scripting.FileSystemObject");
ts = fso.OpenTextFile(file_in, ForReading, true);

var bounds_array = [];

while(!ts.AtEndOfStream){
      s = ts.ReadLine();
      bounds_array = bounds_array.concat(s);
    }

ts.Close();

var x_low = bounds_array[0];
var x_high = bounds_array[1];
var y_low = bounds_array[2];
var y_high = bounds_array[3];
var z_low = bounds_array[4];
var z_high = bounds_array[5];

//Imports 
var DS = WB.AppletList.Applet("DSApplet").App;
//SM = DS.SelectionManager;

//Get the ListView object so we can change the setting for the mesh sizing
var ListView = DS.Script.lv;

//Set Material Properties
//36
var branch = DS.Tree.FirstActiveBranch;

var geomPart = branch.Prototypes;
var count = geomPart.Count;

//cCount = 1;
for( var i=1; i<=count; i++)
{
	var currentGeom = geomPart(i);
    DS.Script.SelectItems(""+currentGeom.ID);//
	part_name = DS.Script.tv.SelectedItem.Tag.Name//
	if (part_name.indexOf("Particle") !== -1) {
		DS.Script.SelectItems(""+currentGeom.ID);
		DS.Script.tv.SelectedItem.Tag.MaterialName = "Copper";
        //DS.Script.SelectItems(""+currentGeom.ID);//
	    //DS.Script.tv.SelectedItem.Tag.MaterialName = 'Adjusted Copper '.concat(cCount.toString());//
	    //cCount=cCount+1;
	}
    if (part_name.indexOf("bubble") !== -1) {
        var bubble_num = i;
    }
    //DS.Script.tv.SelectedItem.Tag.MaterialName = "Copper";//
    //DS.Script.changeActiveObject(currentGeom.ID);
    //part_name = DS.Script.tv.SelectedItem.Tag.Name // delete this when above section is added back in//
    if (part_name == "AirBlock") {  
        DS.Script.SelectItems(""+currentGeom.ID);
	    DS.Script.tv.SelectedItem.Tag.MaterialName = "Air";
       
    } else if (part_name == "GlassBlock") {
        DS.Script.SelectItems(""+currentGeom.ID);
	    DS.Script.tv.SelectedItem.Tag.MaterialName = "Glass";

    }
}

//Done Setting Material Properties

//set thermal cunductance values for contacts
var branch = DS.Tree.FirstActiveBranch;

var contactRegions = branch.ContactRegions;
var count = contactRegions.Count;
//var activeId = DS.Tree.FirstActiveObject.ID;
//80
for( var i=1; i<=count; i++)
{
        var currentRegion = contactRegions(i);
        var sourceString = " ";
        var targetString = " ";		
		
		//testing
		//DS.Script.SelectItems(""+currentRegion.ID);
	    //sourceString = currentRegion.SourceName;
		//targetString = currentRegion.TargetName;
		//sourceGeom = currentRegion.SourceObject;
		//sourceString = DS.Script.tv.SelectedItem.Tag.Name
		//targetGeom = currentRegion.TargetObject;
		//targetString = DS.Script.tv.SelectedItem.Tag.Name
		//end testing
		
		sourceString = currentRegion.SourceName;
		targetString = currentRegion.TargetName;
       
//100
        if ((sourceString.indexOf("Particle") !== -1) && (targetString.indexOf("Particle") !== -1)) // line 100
        {
          DS.Script.SelectItems(""+currentRegion.ID);
          var lGroupDefaults = ListView.FindGroup(3);
          lGroupDefaults.Expand = 1; //Expand group
          ListView.ActivateItem("Thermal Conductance");
          ListView.ItemValue = "Manual";
          ListView.ActivateItem("Thermal Conductance Value");
          ListView.ItemValue = "20000000"; //"750";
          //lGroupDefaults.Expand = 0; //Collapse group 
       
        } else if ((sourceString.indexOf("Air") !== -1) || (targetString.indexOf("Air") !== -1)) {
          DS.Script.SelectItems(""+currentRegion.ID);
          var lGroupDefaults = ListView.FindGroup(3);
          lGroupDefaults.Expand = 1; //Expand group
          ListView.ActivateItem("Thermal Conductance");
          ListView.ItemValue = "Manual";
          ListView.ActivateItem("Thermal Conductance Value");
          ListView.ItemValue = "1.0e11";
          //lGroupDefaults.Expand = 0; //Collapse group

        //} else if (targetString.indexOf("bubble") !== -1) {
        //  DS.Script.SelectItems(""+currentRegion.ID);
        //  DS.Script.doSuppressModelEnvItem(1)

        } else {
          DS.Script.SelectItems(""+currentRegion.ID);
          var lGroupDefaults = ListView.FindGroup(3);
          lGroupDefaults.Expand = 1; //Expand group
          ListView.ActivateItem("Thermal Conductance");
          ListView.ItemValue = "Manual";
          ListView.ActivateItem("Thermal Conductance Value");
          ListView.ItemValue = "10000000";
          //lGroupDefaults.Expand = 0; //Collapse group
        }
        if (targetString.indexOf("bubble") !== -1) {
          DS.Script.SelectItems(""+currentRegion.ID);
          DS.Script.doSuppressModelEnvItem(1)
        
        } else if (sourceString.indexOf("bubble") !== -1) {
          DS.Script.SelectItems(""+currentRegion.ID);
          DS.Script.doSuppressModelEnvItem(1)
        }
}
//DS.Script.doCreateAutomaticConnections(1) //goes after body of influence selection script

// done setting contact thermal conductance

// generate mesh named selection 
name = "NS_Mesh"
NS = DS.Script.addNamedSelection(false,name);
DS.Script.changeActiveObject(NS.ID)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Worksheet";
NS.AddCriteriaData();

NS.GeometryType(0) = DS.Script.id_NS_Body;
NS.Criterion(0) = DS.Script.id_NS_Size;
NS.Operator(0) = DS.Script.id_NS_LessThanEqual;
NS.Value(0) = 10;

NS.AddCriteriaData();
NS.Action(1) = DS.Script.id_NS_Remove;
NS.GeometryType(1) = DS.Script.id_NS_Body;
NS.Criterion(1) = DS.Script.id_NS_Location_Z;
NS.Operator(1) = DS.Script.id_NS_GreaterThanEqual;
NS.Value(1) = z_high; //.055;

NS.AddCriteriaData();
NS.Action(2) = DS.Script.id_NS_Remove;
NS.GeometryType(2) = DS.Script.id_NS_Body;
NS.Criterion(2) = DS.Script.id_NS_Location_Z;
NS.Operator(2) = DS.Script.id_NS_LessThanEqual;
NS.Value(2) = z_low; //.0077;
NS.GenerateFromCriteria()

// Generate Named Selections for Face Meshes
// Air Mesh
name = "NS_Air_Faces"
NS = DS.Script.addNamedSelection(false,name);
DS.Script.changeActiveObject(NS.ID)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Worksheet";
NS.AddCriteriaData();

NS.GeometryType(0) = DS.Script.id_NS_Body;
NS.Criterion(0) = DS.Script.id_NS_NameProperty;
NS.Operator(0) = DS.Script.id_NS_Contains;
NS.StringValue(0) = "AirBlock";

NS.AddCriteriaData();
NS.Action(1) = DS.Script.id_NS_Convert;
NS.GeometryType(1) = DS.Script.id_NS_Face;

NS.AddCriteriaData();
NS.Action(2) = DS.Script.id_NS_Remove;
NS.GeometryType(2) = DS.Script.id_NS_Face;
NS.Criterion(2) = DS.Script.id_NS_Location_X;
//NS.Operator(2) = DS.Script.id_NS_Largest;
NS.Operator(2) = DS.Script.id_NS_Equal;
NS.Value(2) = x_high; // line 200
//202
NS.AddCriteriaData();
NS.Action(3) = DS.Script.id_NS_Remove;
NS.GeometryType(3) = DS.Script.id_NS_Face;
NS.Criterion(3) = DS.Script.id_NS_Location_X;
//NS.Operator(3) = DS.Script.id_NS_Smallest;
NS.Operator(3) = DS.Script.id_NS_Equal;
NS.Value(3) = x_low;

NS.AddCriteriaData();
NS.Action(4) = DS.Script.id_NS_Remove;
NS.GeometryType(4) = DS.Script.id_NS_Face;
NS.Criterion(4) = DS.Script.id_NS_Location_Y;
//NS.Operator(4) = DS.Script.id_NS_Largest;
NS.Operator(4) = DS.Script.id_NS_Equal;
NS.Value(4) = y_low;


NS.AddCriteriaData();
NS.Action(5) = DS.Script.id_NS_Remove;
NS.GeometryType(5) = DS.Script.id_NS_Face;
NS.Criterion(5) = DS.Script.id_NS_Location_Y;
//NS.Operator(5) = DS.Script.id_NS_Smallest;
NS.Operator(5) = DS.Script.id_NS_Equal;
NS.Value(5) = y_high;

NS.AddCriteriaData();
NS.Action(6) = DS.Script.id_NS_Remove;
NS.GeometryType(6) = DS.Script.id_NS_Face;
NS.Criterion(6) = DS.Script.id_NS_Location_Z;
NS.Operator(6) = DS.Script.id_NS_LessThanEqual;
NS.Value(6) = z_low; //.0077;

NS.AddCriteriaData();
NS.Action(7) = DS.Script.id_NS_Remove;
NS.GeometryType(7) = DS.Script.id_NS_Face;
NS.Criterion(7) = DS.Script.id_NS_Location_Z;
NS.Operator(7) = DS.Script.id_NS_GreaterThanEqual;
NS.Value(7) = z_high; //.0077;
NS.GenerateFromCriteria()

//Particle Mesh
name = "NS_Particle_Faces"
NS = DS.Script.addNamedSelection(false,name);
DS.Script.changeActiveObject(NS.ID)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Worksheet";
NS.AddCriteriaData();

NS.GeometryType(0) = DS.Script.id_NS_Body;
NS.Criterion(0) = DS.Script.id_NS_NameProperty;
NS.Operator(0) = DS.Script.id_NS_Contains;
NS.StringValue(0) = "Particle";

NS.AddCriteriaData();
NS.Action(1) = DS.Script.id_NS_Convert;
NS.GeometryType(1) = DS.Script.id_NS_Face;
NS.GenerateFromCriteria()

//Get 'Mesh' control group
var Mesh_Mod = DS.Tree.FirstActiveBranch.MeshControlGroup;

//Select 'Mesh' from the tree
DS.Script.SelectItems(""+Mesh_Mod.ID);

//Set global mesh options

// Turn off quality checking
var lGroupDefaults = ListView.FindGroup(4); // select surface mesher parameter
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Check Mesh Quality"); //Set 'Physics Preference' option to 'CFD'
ListView.ItemValue = "No";
ListView.ActivateItem("Target Quality"); //Set 'Physics Preference' option to 'CFD'
ListView.ItemValue = "0.005";

//275
//Set Advancing Front
var lGroupDefaults = ListView.FindGroup(6); // select surface mesher parameter
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Triangle Surface Mesher"); //Set 'Physics Preference' option to 'CFD'
ListView.ItemValue = "Advancing Front";
//lGroupDefaults.Expand = 0; //Collapse group

// set defeaturing size
var lGroupDefaults = ListView.FindGroup(3);
lGroupDefaults.Expand = 1;
ListView.ActivateItem("Defeature Size");
ListView.ItemValue = "1.0E-7";  // line 278

//set adaptive/growthrate/proximity/curvature/mins
var lGroupDefaults = ListView.FindGroup(3);
lGroupDefaults.Expand = 1;
ListView.ActivateItem("Use Adaptive Sizing");
ListView.ItemValue = "No";
//ListView.ActivateItem("Growth Rate");
//ListView.ItemValue = "1.35";
ListView.ActivateItem("Capture Curvature");
ListView.ItemValue = "No";
//ListView.ActivateItem("Curvature Min Size");
//ListView.ItemValue = "4.0E-7"; //6.0E-7 for both
ListView.ActivateItem("Capture Proximity"); //300
ListView.ItemValue = "Yes";
ListView.ActivateItem("Proximity Min Size");
ListView.ItemValue = "1.2E-7";

//patch convergent/indepenent tetrahedral meshing and adjustable body sizing -- IMPORTANT
//DS.script.doInsertMeshElementShape(1)
//var lGroupDefaults = ListView.FindGroup(1); 
//lGroupDefaults.Expand = 1; //Expand group
//ListView.ActivateItem("Scoping Method");
//ListView.ItemValue = "Named Selection" ;
//ListView.ActivateItem("Named Selection");
//ListView.ItemValue = "NS_Mesh";

//var lGroupDefaults = ListView.FindGroup(2); //patch independent vs patch dependent
//lGroupDefaults.Expand = 1; //Expand group
//ListView.ActivateItem("Method");
//ListView.ItemValue = "Tetrahedrons"
//ListView.ActivateItem("Algorithm");
//ListView.ItemValue = "Patch Conforming"
//ListView.ItemValue = "Patch Independent"
//var lGroupDefaults = ListView.FindGroup(3); 
//lGroupDefaults.Expand = 1; //Expand group
//ListView.ActivateItem("Min Size Limit");
//ListView.ItemValue = ".005"

//Body of Influence ("bubble")
DS.script.doInsertMeshSize(1)
var lGroupDefaults = ListView.FindGroup(1); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Mesh";
var lGroupDefaults = ListView.FindGroup(2); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Type");
ListView.ItemValue = "Body of Influence"

var geomPart = branch.Prototypes;
DS.SelectionManager.Clear();
DS.SelectionManager.ForceSelect(geomPart(bubble_num).Part.ID, geomPart(bubble_num).topoID);
//342
ListView.ActivateItem("Bodies of Influence")
ListView.ItemValue = "Apply"
ListView.ActivateItem("Element Size")
ListView.ItemValue = "8E-6" //7.0E-6 //346
DS.SelectionManager.Clear();

//Face Sizings
//Particles
DS.script.doInsertMeshSize(1)
var lGroupDefaults = ListView.FindGroup(1); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Particle_Faces";
var lGroupDefaults = ListView.FindGroup(2); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Type");
ListView.ItemValue = "Element Size"
ListView.ActivateItem("Element Size")
ListView.ItemValue = "7E-6" //8E-6 //363

//Air
DS.script.doInsertMeshSize(1)
var lGroupDefaults = ListView.FindGroup(1); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Air_Faces";

var lGroupDefaults = ListView.FindGroup(2); 
lGroupDefaults.Expand = 1; //Expand group //375
ListView.ActivateItem("Type");
ListView.ItemValue = "Element Size"
ListView.ActivateItem("Element Size")
ListView.ItemValue = "4.0E-6" //8E-6

var lGroupDefaults = ListView.FindGroup(3);
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Capture Curvature");
ListView.ItemValue = "Yes"
ListView.ActivateItem("Capture Proximity");
ListView.ItemValue = "Yes"
ListView.ActivateItem("Local Min Size");
ListView.ItemValue = "4.0E-7" //388
ListView.ActivateItem("Proximity Min Size");
ListView.ItemValue = "1.2E-7"


//
// done with mesh setup
//

//
//
// Named Selection Heat Flux
//400
name = "NS_Heat_Flux"
NS = DS.Script.addNamedSelection(false,name);
DS.Script.changeActiveObject(NS.ID)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Worksheet";

NS.AddCriteriaData();
NS.GeometryType(0) = DS.Script.id_NS_Body;
NS.Criterion(0) = DS.Script.id_NS_NameProperty //id_NS_MaterialName;
NS.Operator(0) = DS.Script.id_NS_Contains;
NS.StringValue(0) = "Particle";

NS.AddCriteriaData();
NS.Action(1) = DS.Script.id_NS_Convert;
NS.GeometryType(1) = DS.Script.id_NS_Face;

NS.AddCriteriaData(); //
NS.Action(2) = DS.Script.id_NS_Filter;
NS.GeometryType(2) = DS.Script.id_NS_Face;
NS.Criterion(2) = DS.Script.id_NS_Location_Y
//NS.Operator(2) = DS.Script.id_NS_Largest
NS.Operator(2) = DS.Script.id_NS_Equal;
NS.Value(2) = y_high;

NS.GenerateFromCriteria();

var lGroupDefaults = ListView.FindGroup(3); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Surface Area");
ListView.SelectedItem.IsChecked="true"
//
//
//

// Named selection temperature particles only
name = "NS_Part_Temp"
NS = DS.Script.addNamedSelection(false,name);
DS.Script.changeActiveObject(NS.ID)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Worksheet";

NS.AddCriteriaData();
NS.GeometryType(0) = DS.Script.id_NS_Body;
NS.Criterion(0) = DS.Script.id_NS_NameProperty //id_NS_NameProperty;
NS.Operator(0) = DS.Script.id_NS_Contains;
NS.StringValue(0) = "Particle";

NS.AddCriteriaData();
NS.Action(1) = DS.Script.id_NS_Convert;
NS.GeometryType(1) = DS.Script.id_NS_Face;

NS.AddCriteriaData(); // exclude tiny singe triangles -- only focus on major faces
NS.Action(2) = DS.Script.id_NS_Filter;
NS.GeometryType(2) = DS.Script.id_NS_Face;
NS.Criterion(2) = DS.Script.id_NS_Location_Y
//NS.Operator(2) = DS.Script.id_NS_Smallest
NS.Operator(2) = DS.Script.id_NS_Equal;
NS.Value(2) = y_low;
NS.GenerateFromCriteria();

// Named Selection Entire Hot Face
name = "NS_Hot_Face"
NS = DS.Script.addNamedSelection(false,name);
DS.Script.changeActiveObject(NS.ID)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Worksheet";

NS.AddCriteriaData();
NS.GeometryType(0) = DS.Script.id_NS_Face;
NS.Criterion(0) = DS.Script.id_NS_Location_Y
//NS.Operator(0) = DS.Script.id_NS_Largest
NS.Operator(0) = DS.Script.id_NS_Equal;
NS.Value(0) = y_high;

NS.AddCriteriaData();
NS.Action(1) = DS.Script.id_NS_Remove;
NS.GeometryType(1) = DS.Script.id_NS_Face;
NS.Criterion(1) = DS.Script.id_NS_Location_Z;
NS.Operator(1) = DS.Script.id_NS_GreaterThanEqual;
NS.Value(1) = z_high;

NS.AddCriteriaData();
NS.Action(2) = DS.Script.id_NS_Remove;
NS.GeometryType(2) = DS.Script.id_NS_Face;
NS.Criterion(2) = DS.Script.id_NS_Location_Z;
NS.Operator(2) = DS.Script.id_NS_LessThanEqual;
NS.Value(2) = z_low;

NS.GenerateFromCriteria();

// Named Selection Temperature Face
name = "NS_Temperature"
NS = DS.Script.addNamedSelection(false,name);
DS.Script.changeActiveObject(NS.ID)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Worksheet";

NS.AddCriteriaData();
NS.GeometryType(0) = DS.Script.id_NS_Face;
NS.Criterion(0) = DS.Script.id_NS_Location_Y
//NS.Operator(0) = DS.Script.id_NS_Smallest
NS.Operator(0) = DS.Script.id_NS_Equal;
NS.Value(0) = y_low;
//504
NS.AddCriteriaData();
NS.Action(1) = DS.Script.id_NS_Remove;
NS.GeometryType(1) = DS.Script.id_NS_Face;
NS.Criterion(1) = DS.Script.id_NS_Location_Z;
NS.Operator(1) = DS.Script.id_NS_GreaterThanEqual;
NS.Value(1) = z_high;

NS.AddCriteriaData();
NS.Action(2) = DS.Script.id_NS_Remove;
NS.GeometryType(2) = DS.Script.id_NS_Face;
NS.Criterion(2) = DS.Script.id_NS_Location_Z;
NS.Operator(2) = DS.Script.id_NS_LessThanEqual;
NS.Value(2) = z_low;

NS.GenerateFromCriteria();
//520
var lGroupDefaults = ListView.FindGroup(3); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Surface Area");
ListView.SelectedItem.IsChecked="true"

//name = "NS_Radiation"
//NS = DS.Script.addNamedSelection(false,name);
//DS.Script.changeActiveObject(NS.ID)
//ListView.ActivateItem("Scoping Method");
//ListView.ItemValue = "Worksheet";

//NS.AddCriteriaData();
//NS.GeometryType(0) = DS.Script.id_NS_Face;
//NS.Criterion(0) = DS.Script.id_NS_Size;
//NS.Operator(0) = DS.Script.id_NS_LessThanEqual;
//NS.Value(0) = .0001;
//NS.GenerateFromCriteria();

// Creating Heat Flux B.C
var Env = DS.Tree.FirstActiveBranch.Environment;
DS.Script.SelectItems(""+Env.ID);

//Creating heat flux BC
DS.Script.doInsertEnvironmentHeatFlux(1)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Heat_Flux" ;
ListView.ActivateItem("Magnitude");
ListView.ItemValue = "10000000000"
ListView.SelectedItem.IsChecked="true" // Might need to be supressed = false... 

//Creating temperature BC
DS.Script.doInsertEnvironmentKnownTemperature(1)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Temperature" ;
ListView.ActivateItem("Magnitude");
ListView.ItemValue = "22"
ListView.SelectedItem.IsChecked="true"

//Creating radiation BC on nanoparticle surfaces
//DS.Script.doInsertEnvironmentRadiation(1)
//ListView.ActivateItem("Scoping Method");
//ListView.ItemValue = "Named Selection" ;
//ListView.ActivateItem("Named Selection");
//ListView.ItemValue = "NS_Radiation" ;
//ListView.SelectedItem.IsChecked="true" // Might need to be supressed = false...
// done with boundary conditions


//Solution
var Sol_eqv = DS.Tree.FirstActiveBranch.Environment.AnswerSet;
DS.Script.SelectItems(""+Sol_eqv.ID);
//Inserting Temperature Result
//577
//Inserting Temperature Results
// Heat Flux NS Results
DS.Script.doSolutionInsertThermalResult(DS.Script.id_Temperature, 0);
var lGroupDefaults = ListView.FindGroup(1); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Heat_Flux";

//DS.Script.doCalculateResults(1)
//DS.Script.doSolveDefaultHandler(1)

//var result_1 = filepath.concat("Temperature_Results_Particle_Faces_Hot");
//DS.Script.doExportToTextFile(result_1)

// Particle Temp NS Results
DS.Script.doSolutionInsertThermalResult(DS.Script.id_Temperature, 0);
var lGroupDefaults = ListView.FindGroup(1); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Part_Temp";

//DS.Script.doCalculateResults(1)
//DS.Script.doSolveDefaultHandler(1)

//var result_2 = filepath.concat("Temperature_Results_Particle_Faces_Cold");
//DS.Script.doExportToTextFile(result_2)


// Hot Face NS Results
DS.Script.doSolutionInsertThermalResult(DS.Script.id_Temperature, 0);
var lGroupDefaults = ListView.FindGroup(1); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Hot_Face";

//DS.Script.doCalculateResults(1)
//DS.Script.doSolveDefaultHandler(1)

//var result_3 = filepath.concat("Temperature_Results_Hot");
//DS.Script.doExportToTextFile(result_3)

//NS_Temperature Results
DS.Script.doSolutionInsertThermalResult(DS.Script.id_Temperature, 0);
var lGroupDefaults = ListView.FindGroup(1); 
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "NS_Temperature";

//DS.Script.doCalculateResults(1)
//DS.Script.doSolveDefaultHandler(1)

//var result_4 = filepath.concat("Temperature_Results_Cold");
//DS.Script.doExportToTextFile(result_4)

var branch = DS.Tree.FirstActiveBranch;
var geomPart = branch.Prototypes;
var count = geomPart.Count;
for( var i=1; i<=count; i++)
{
    DS.SelectionManager.Clear();
    var currentGeom = geomPart(i);
    DS.Script.SelectItems(""+currentGeom.ID);//
    part_name = DS.Script.tv.SelectedItem.Tag.Name//
    if (part_name.indexOf("bubble") !== -1) {
    var emp = 0;    
    } else {    
        //var currentGeom = geomPart(i);
        //DS.Script.SelectItems(""+currentGeom.ID);
        DS.Script.doMeshGenerationsSuccessful()
    }
}
