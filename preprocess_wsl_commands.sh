#!/bin/bash

#wsl  cat "generated_ast_dataset/train_ast.raw.txt"
#base command  wsl "cat generated_ast_dataset/train_ast.raw.txt | cut -d' ' -f1 | tr '|' '\n' | awk  '{n[/bin/bash]++} END {for (i in n) print i,n[i]}' > generated_ast_dataset/train_ast.histo.tgt.c2s"

cat generated_ast_dataset/train_ast.raw.txt | cut -d' ' -f1 | tr '|' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' > generated_ast_dataset/train_ast.histo.tgt.c2s

cat generated_ast_dataset/train_ast.raw.txt | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f1,3 | tr ',|' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' > generated_ast_dataset/train_ast.histo.ori.c2s

cat generated_ast_dataset/train_ast.raw.txt | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f2 | tr '|' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' > generated_ast_dataset/train_ast.histo.node.c2s

