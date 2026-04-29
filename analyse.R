library(ggplot2)
library(dplyr)

# Charger les données
data <- read.csv("data/export.csv")

# Aperçu
head(data)

# Statistiques simples
summary(data)

# Budget moyen
mean(data$budget, na.rm = TRUE)

# Graphique budget
ggplot(data, aes(x = budget)) +
  geom_histogram(binwidth = 1000, fill = "blue")

# Répartition opérateurs
ggplot(data, aes(x = operateur)) +
  geom_bar(fill = "green")

# Temps en ligne par sexe
ggplot(data, aes(x = sexe, y = temps_online)) +
  geom_boxplot()
  
print("heyy !!")
