library(ggplot2)
library(reshape2)
library(stringr) 

setwd("E://Projects//Dashboard-For-VQA//Paper files//")

data <- read.csv("NASA-TLX.csv")


long_data <- reshape2::melt(data)


long_data$variable <- str_replace_all(str_wrap(gsub("\\.", " ", long_data$variable), width = 15), "\\.", " ")


long_data$variable <- factor(long_data$variable, levels = unique(long_data$variable))

ggplot(long_data, aes(x = variable, y = value)) +
  geom_boxplot(fill = '#888888') +
  theme_minimal() +
  theme(
    axis.text.x = element_text(
      angle = 0,
      hjust = 0.5,
      vjust = 1,  # Adjust vertical justification to make labels span two rows
      lineheight = 0.8,  # Adjust line height
      size = 20  # Increase font size
    ),
    axis.text.y = element_text(
      angle = 0,
      hjust = 0.5,
      vjust = 1,  # Adjust vertical justification
      lineheight = 0.8,  # Adjust line height
      size = 20  # Set the same font size as axis.text.x
    ),
    legend.position = "none",
    plot.title = element_text(face = "bold", hjust = 0.5, size = 26),  # Center-aligned plot title
    axis.title.x = element_blank(),  # Blank x-axis title
    axis.title.y = element_text(face = "bold", hjust = 0.5, size = 24, margin = margin(r = 20))  # Center-aligned Y-axis title with margin
  ) +
  labs(
    title = "NASA-TLX Load Indices for Using Tag-Board",  # Plot title
    x = "Factors",  # X-axis title
    y = "Load Index"  # Y-axis title
  )
