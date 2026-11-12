# Step 2 Report: Data Drift Analysis

## Method

The reproducible analysis in [`src/drift.py`](../src/drift.py) compares each year from 2015-2021 with 2014, separately for pooled apps, goodware, and malware. It runs a two-sided, two-sample Kolmogorov-Smirnov (KS) test on each of the 1,848 API-call features. The KS statistic is the maximum absolute difference between the two empirical cumulative distribution functions (an effect size from 0 to 1).

P-values use SciPy's asymptotic method. Benjamini-Hochberg false discovery rate correction is performed over the 1,848 feature tests within each comparison year and scope. Adjusted p-values (`q`) at or below 0.05 are called significant. The yearly drift ranking uses mean KS statistic across features, rather than p-values alone, so large sample sizes do not define practical importance. Inputs are validated through the Step 1 loader. Values that underflow to zero are displayed as `<1e-300`. No random sampling or fitting is used.

Reproduce from the project directory with:

```bash
python -m src.drift
```

## Years that differ most from 2014

Ranked by mean feature-wise KS statistic (largest first). Significant features are those passing the within-comparison Benjamini-Hochberg correction.

| Scope | Year | Median KS | Mean KS | Max KS | Significant features |
|---|---:|---:|---:|---:|---:|
| goodware | 2020 | 0.000556 | 0.063169 | 0.9387 | 410 / 1,848 |
| goodware | 2021 | 0.001000 | 0.062619 | 0.9553 | 427 / 1,848 |
| goodware | 2019 | 0.000667 | 0.050292 | 0.8327 | 387 / 1,848 |
| goodware | 2018 | 0.000222 | 0.039062 | 0.7427 | 376 / 1,848 |
| goodware | 2017 | 0.000111 | 0.032201 | 0.6476 | 326 / 1,848 |
| goodware | 2016 | 0.000111 | 0.029134 | 0.6160 | 288 / 1,848 |
| goodware | 2015 | 0.000111 | 0.017991 | 0.4197 | 237 / 1,848 |
| malware | 2021 | 0.000111 | 0.061471 | 0.6157 | 395 / 1,848 |
| malware | 2020 | 0.000111 | 0.057156 | 0.8289 | 343 / 1,848 |
| malware | 2019 | 0.000222 | 0.054967 | 0.7919 | 322 / 1,848 |
| malware | 2018 | 0.000222 | 0.038990 | 0.6004 | 433 / 1,848 |
| malware | 2017 | 0.000111 | 0.034134 | 0.5743 | 418 / 1,848 |
| malware | 2016 | 0.000222 | 0.027418 | 0.3384 | 415 / 1,848 |
| malware | 2015 | 0.000111 | 0.022018 | 0.3550 | 353 / 1,848 |
| overall | 2021 | 0.000667 | 0.052296 | 0.6924 | 459 / 1,848 |
| overall | 2020 | 0.000333 | 0.037271 | 0.4678 | 433 / 1,848 |
| overall | 2019 | 0.000333 | 0.031329 | 0.4564 | 393 / 1,848 |
| overall | 2018 | 0.000222 | 0.026313 | 0.5198 | 448 / 1,848 |
| overall | 2017 | 0.000167 | 0.025939 | 0.5243 | 423 / 1,848 |
| overall | 2016 | 0.000167 | 0.022245 | 0.4582 | 416 / 1,848 |
| overall | 2015 | 0.000111 | 0.013902 | 0.2608 | 346 / 1,848 |

## Features with the largest drift

For each scope, features are ranked by their maximum KS statistic across the seven comparisons. The listed year is where that maximum occurred; `q` is its adjusted p-value for that year and scope.

### Overall

| Feature | Year | KS statistic | Raw p-value | Adjusted q-value |
|---|---:|---:|---:|---:|
| `Landroid/content/ContentResolver;.query:(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;Landroid/os/CancellationSignal;)Landroid/database/Cursor;` | 2021 | 0.6924 | <1e-300 | <1e-300 |
| `Landroid/content/ContentResolver;.openFileDescriptor:(Landroid/net/Uri;Ljava/lang/String;Landroid/os/CancellationSignal;)Landroid/os/ParcelFileDescriptor;` | 2021 | 0.6699 | <1e-300 | <1e-300 |
| `Landroid/os/Process;.myPid:()I` | 2021 | 0.6551 | <1e-300 | <1e-300 |
| `Ljava/lang/String;.getBytes:(Ljava/nio/charset/Charset;)[B` | 2021 | 0.6421 | <1e-300 | <1e-300 |
| `Landroid/os/PowerManager$WakeLock;.acquire:(J)V` | 2021 | 0.6252 | <1e-300 | <1e-300 |
| `Landroid/content/Context;.getApplicationInfo:()Landroid/content/pm/ApplicationInfo;` | 2021 | 0.6118 | <1e-300 | <1e-300 |
| `Landroid/os/Handler;.obtainMessage:(IIILjava/lang/Object;)Landroid/os/Message;` | 2021 | 0.6102 | <1e-300 | <1e-300 |
| `Landroid/app/NotificationManager;.notify:(Ljava/lang/String;ILandroid/app/Notification;)V` | 2021 | 0.5913 | <1e-300 | <1e-300 |
| `Landroid/os/Handler;.obtainMessage:(III)Landroid/os/Message;` | 2021 | 0.5878 | <1e-300 | <1e-300 |
| `Ljava/lang/String;.valueOf:(Ljava/lang/Object;)Ljava/lang/String;` | 2021 | 0.5685 | <1e-300 | <1e-300 |

### Goodware

| Feature | Year | KS statistic | Raw p-value | Adjusted q-value |
|---|---:|---:|---:|---:|
| `Landroid/content/ContentResolver;.query:(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;` | 2021 | 0.9553 | <1e-300 | <1e-300 |
| `Landroid/content/ContentResolver;.query:(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;Landroid/os/CancellationSignal;)Landroid/database/Cursor;` | 2021 | 0.9000 | <1e-300 | <1e-300 |
| `Landroid/os/Process;.myPid:()I` | 2021 | 0.8893 | <1e-300 | <1e-300 |
| `Landroid/content/ContentResolver;.openFileDescriptor:(Landroid/net/Uri;Ljava/lang/String;Landroid/os/CancellationSignal;)Landroid/os/ParcelFileDescriptor;` | 2021 | 0.8587 | <1e-300 | <1e-300 |
| `Landroid/content/Context;.getApplicationInfo:()Landroid/content/pm/ApplicationInfo;` | 2021 | 0.8483 | <1e-300 | <1e-300 |
| `Ljava/lang/String;.getBytes:(Ljava/nio/charset/Charset;)[B` | 2021 | 0.8316 | <1e-300 | <1e-300 |
| `Landroid/os/PowerManager$WakeLock;.acquire:(J)V` | 2021 | 0.8112 | <1e-300 | <1e-300 |
| `Landroid/os/Handler;.obtainMessage:(IIILjava/lang/Object;)Landroid/os/Message;` | 2021 | 0.7984 | <1e-300 | <1e-300 |
| `Landroid/app/NotificationManager;.notify:(Ljava/lang/String;ILandroid/app/Notification;)V` | 2021 | 0.7941 | <1e-300 | <1e-300 |
| `Landroid/os/Handler;.obtainMessage:(III)Landroid/os/Message;` | 2020 | 0.7346 | <1e-300 | <1e-300 |

### Malware

| Feature | Year | KS statistic | Raw p-value | Adjusted q-value |
|---|---:|---:|---:|---:|
| `Ljava/lang/StringBuilder;.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;` | 2020 | 0.8289 | <1e-300 | <1e-300 |
| `Ljava/lang/StringBuilder;.append:(Ljava/lang/Object;)Ljava/lang/StringBuilder;` | 2020 | 0.8273 | <1e-300 | <1e-300 |
| `Ljava/lang/String;.substring:(II)Ljava/lang/String;` | 2020 | 0.8262 | <1e-300 | <1e-300 |
| `Ljava/lang/StringBuilder;.append:(J)Ljava/lang/StringBuilder;` | 2020 | 0.8188 | <1e-300 | <1e-300 |
| `Ljava/lang/String;.getBytes:()[B` | 2020 | 0.8188 | <1e-300 | <1e-300 |
| `Ljava/io/File;.exists:()Z` | 2020 | 0.8100 | <1e-300 | <1e-300 |
| `Ljava/lang/StringBuilder;.append:(I)Ljava/lang/StringBuilder;` | 2020 | 0.7929 | <1e-300 | <1e-300 |
| `Landroid/content/Context;.startActivity:(Landroid/content/Intent;)V` | 2019 | 0.7919 | <1e-300 | <1e-300 |
| `Ljava/io/File;.delete:()Z` | 2020 | 0.7897 | <1e-300 | <1e-300 |
| `Ljava/lang/String;.substring:(I)Ljava/lang/String;` | 2020 | 0.7829 | <1e-300 | <1e-300 |

## Interpretation and limitations

The tests quantify feature-distribution drift relative to 2014; they do not establish concept drift or show that a model's predictive accuracy changed. The class-specific results help separate within-class feature changes from changes in the pooled distribution. API-call counts are discrete and tied, whereas the classical KS p-value calibration assumes continuous distributions; interpret p-values cautiously and use KS statistics as descriptive effect sizes. The asymptotic approximation and correction method are fixed in code for reproducibility.
