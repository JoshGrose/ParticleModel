//filepaths
var curr_dir = "//work//07329//joshg//stampede2//simulations//ParticleModel//sensitivity//mesh_results//meshResult_timestep2_final"
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

var result_1 = filepath.concat("//TempResults_FaceSizing_Index_5");
DS.Script.doExportToTextFile(result_1)

