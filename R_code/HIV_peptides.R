df.epi <- read.csv("data/ctl_variant.csv", header=T)

df.epi <- df.epi[grep("^[ACDEFGHIKLMNPQRSTVWY]\\d+[ACDEFGHIKLMNPQRSTVWY]$", df.epi$Mutation_epitope),]
df.epi <- df.epi[grep("^[ACDEFGHIKLMNPQRSTVWY]+$", df.epi$Epitope),]
len <- function(x) nchar(as.character(x))

df.epi$codes <- sapply(df.epi$Mutation_Type_Code, function(x) strsplit(as.character(x),", "))

isescape <- function(x) "E" %in% x || "LE" %in% x || "IE" %in% x || "NSF" %in% x

df.epi$type <- sapply(df.epi$codes,
                      function(x) ifelse("TCR" %in% x, "tcr",
                                  ifelse("DHB" %in% x, "hla",
                                  ifelse(isescape(x), "unknown",
                                                      "non-escape"
                                                ))))

df.epi <- subset(df.epi, type = "hla")

df.epi <- data.frame(binder = df.epi$Epitope,
                     non_binder = df.epi$Variant_Epitope,
                     mhc = df.epi$HLA,
                     check.names = TRUE
                     )
View(df.epi)
write.csv(df.epi, "data/HIV_peptides.csv")
