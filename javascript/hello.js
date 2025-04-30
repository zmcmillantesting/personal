const prompt = require("prompt-sync")();

let statement = prompt("Please enter a statement: ");
print_Statement(statement);

function print_Statement(statement) {
  if (statement !== "") {
    console.log(statement);
  } else {
    console.log("The statement is blank");
  }
}