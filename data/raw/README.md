# Raw dataset provenance

This is `student-por.csv`, the Portuguese-language subset of the UCI Student Performance dataset (649 observations, 33 variables). UCI repository record: https://archive.ics.uci.edu/dataset/320/student%2Bperformance

The bundled raw copy was obtained from the public GitHub mirror at https://raw.githubusercontent.com/aysh0220/DATA-SCIENCE/master/student-por.csv because the UCI archive download endpoint was unavailable in this environment. The mirror file has comma delimiters; the official archive copy uses semicolons. Its header, 649-row count, 33-column count, and fields match the UCI Portuguese-course file. This is a public third-party mirror, not a synthetic or newly collected dataset. For strict source-chain verification, replace this file with `student-por.csv` downloaded directly from UCI; the loader accepts either delimiter.

The source paper describes two Portuguese secondary schools and collection during 2005–2006. The record has no student ID. Cite: P. Cortez and A. Silva, “Using Data Mining to Predict Secondary School Student Performance,” 2008, DOI: 10.1109/FIE.2008.4720288.
