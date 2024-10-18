async function createRule() {
    const ruleString = document.getElementById('ruleString').value;
    
    const response = await fetch('/create_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_string: ruleString })
    });
    
    const result = await response.json();
    alert(JSON.stringify(result));
}

async function evaluateRule() {
    const userData = document.getElementById('userData').value;
    const ruleAST = document.getElementById('ruleAST').value;

    const response = await fetch('/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_data: JSON.parse(userData),
            rule_ast: JSON.parse(ruleAST)
        })
    });

    const result = await response.json();
    document.getElementById('result').innerText = JSON.stringify(result);
}
