# Composite PD-code list

PD-code representatives for the organization's complete 1,783-name catalog of
knots with at most 11 crossings, including prime knots, mirror names,
composites, and the unknot.

## Data

`data/com_pd_code_list.txt` contains one record per line:

```text
[KNOT_NAME|[[a, b, c, d], ...]]
```

The committed file contains 1,783 records. `K0a1` uses the empty code `[]`.
The PD codes are usable representatives; downstream tools should validate any
strong planarity or orientation assumptions they additionally require.

## Regeneration

`data/get_pd_code_list.py` reads the prime baseline in
`data/pd_code_list.txt`, mirrors prime diagrams when a name begins with `m`,
and asks SageMath to form connected sums for composite names. Text data is
parsed with `ast.literal_eval`.

```bash
sage -python data/get_pd_code_list.py
```

The script writes to `data/com_pd_code_list.txt` regardless of the caller's
working directory.

## Consuming the table

Use `rsplit("|", 1)` only for value/name tables; this name/PD table should be
split once from the left because the PD expression contains no pipe symbols.

## License

MIT. See `LICENSE`.

