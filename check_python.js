var spawn = require("child_process").spawn;

var process = spawn('python',["./home/marco/trazdia/collector/trazdia.py", 'Diario_Oficial_SP', '01/03/2017']);
process.stdout.on('data', function (data){
  print(data);
});
