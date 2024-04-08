#!/usr/bin/env pwsh

$env:jj2_lsp = "#@jj2"

python ../../bin/io/render-jj2.py *.jj2
