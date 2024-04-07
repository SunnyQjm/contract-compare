
#!/bin/bash

result_dir=/root/results
input_dir=/root/inputs
rules_dir=/root/TxSpector/detector/rules

# Define a array store all rule names, except opcode.dl and types.dl
rule_targets=(`ls $rules_dir | grep -vE "opcode.dl|types.dl"`)
# rule_targets=1Reentrancy.dl

analyze_geth_bin=/root/TxSpector/detector/bin/analyze_geth.sh

function do_test() {
    item_dir=$1
    item_name=$(basename $item_dir)
    trace_file=$item_dir/$item_name.txt
    sc_addr_facts_file=$item_dir/sc_addr.facts

    if [ -f $item_dir/.done ]; then
        echo "Skip $item_name"
        return
    fi

    # Generate dir in results
    result_item_dir=$result_dir/$item_name
    mkdir -p $result_item_dir

    pushd $result_item_dir
    # Run the test
    $analyze_geth_bin $trace_file facts

    # cp sc_addr_facts_file to result_item_dir if file exists
    mkdir -p $result_item_dir/facts
    if [ -f $sc_addr_facts_file ]; then
        cp $sc_addr_facts_file $result_item_dir/facts
    else
        echo "" > $result_item_dir/facts/sc_addr.facts
    fi

    for rule_target in ${rule_targets[@]}; do
        rule_file=$rules_dir/$rule_target
        rule_name=$(basename $rule_target .dl)
        echo "Running rule $rule_name"
        mkdir -p $rule_name
        pushd $rule_name
        souffle -F ../facts $rule_file
        popd
    done
    popd
    echo "done" > $item_dir/.done
}

for item_dir in $input_dir/*; do
    do_test $item_dir
done