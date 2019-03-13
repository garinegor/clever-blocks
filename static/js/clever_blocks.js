function postCode(){
	var code = Blockly.Python.workspaceToCode(workspace);
	$.post("/run", 
			{
				code: code
			},
			onSuccess);
	function onSuccess(){
		return;
	}
}

var blocklyArea = document.getElementById('blocklyArea');
var blocklyDiv = document.getElementById('blocklyDiv');
var workspace = Blockly.inject(blocklyDiv,{toolbox: document.getElementById('toolbox'), scrollbars: true});
var onresize = function(e) {
	// Compute the absolute coordinates and dimensions of blocklyArea.
	var element = blocklyArea;
	var x = 0;
	var y = 0;
	do {
		x += element.offsetLeft;
		y += element.offsetTop;
		element = element.offsetParent;
	} while (element);
	// Position blocklyDiv over blocklyArea.
	blocklyDiv.style.left = x + 'px';
	blocklyDiv.style.top = y + 'px';
	blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
	blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
	Blockly.svgResize(workspace);
};
window.addEventListener('resize', onresize, false);
onresize();
Blockly.svgResize(workspace);

