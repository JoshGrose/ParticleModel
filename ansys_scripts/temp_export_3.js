//filepaths
curr_dir = "PATH"
var filepath = curr_dir // '//work//07329//joshg//stampede2//simulations//ParticleModel//ansys_scripts//NanoparticleOutput//Results4//';

var DS = WB.AppletList.Applet("DSApplet").App;
var ListView = DS.Script.lv;
var branch = DS.Tree.FirstActiveBranch;

var Sol_eqv = DS.Tree.FirstActiveBranch.Environment.AnswerSet;
DS.Script.SelectItems(""+Sol_eqv.ID);

DS.Script.doSolutionInsertThermalResult(DS.Script.id_Temperature, 0);
var lGroupDefaults = ListView.FindGroup(1);
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");           
ListView.ItemValue = "NS_Heat_Flux";

DS.Script.doCalculateResults(1)
DS.Script.doSolveDefaultHandler(1)

var result_1 = filepath.concat("//Temperature_Results_Particle_Faces_Hot");
DS.Script.doExportToTextFile(result_1)

