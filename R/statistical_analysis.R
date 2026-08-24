library(tidyverse)
library(lubridate)

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
base <- if (length(script_arg) > 0) {
  dirname(dirname(normalizePath(sub("^--file=", "", script_arg[1]))))
} else {
  normalizePath(getwd())
}
dir.create(file.path(base, "visualisations"), showWarnings = FALSE)
customers <- read_csv(file.path(base,"data","customers.csv"))
products <- read_csv(file.path(base,"data","products.csv"))
orders <- read_csv(file.path(base,"data","orders.csv"))

sales <- orders %>%
  left_join(customers, by="CustomerID") %>%
  left_join(products, by="ProductID") %>%
  mutate(
    OrderDate = as.Date(OrderDate),
    Revenue = Quantity * UnitPrice * (1 - Discount),
    Cost = Quantity * UnitCost,
    Profit = Revenue - Cost,
    ProfitMargin = if_else(Revenue != 0, Profit/Revenue*100, 0)
  )

# Statistical relationship between discount and profit
correlation <- cor(sales$Discount, sales$Profit, use="complete.obs")
print(paste("Discount-Profit correlation:", round(correlation,4)))

model <- lm(Profit ~ Discount + Quantity + UnitPrice, data=sales)
print(summary(model))

# Visualization
p <- ggplot(sales, aes(x=Discount, y=Profit)) +
  geom_point(alpha=0.25) +
  geom_smooth(method="lm", se=TRUE) +
  labs(title="Relationship Between Discount and Profit",
       x="Discount", y="Profit (ZAR)") +
  theme_minimal()

ggsave(file.path(base,"visualisations","discount_profit_regression.png"),
       p, width=9, height=5, dpi=150)

# Category comparison
category <- sales %>%
  group_by(Category) %>%
  summarise(Revenue=sum(Revenue), Profit=sum(Profit), .groups="drop")

p2 <- ggplot(category, aes(x=reorder(Category, Profit), y=Profit)) +
  geom_col() +
  coord_flip() +
  labs(title="Profit by Product Category", x="Category", y="Profit (ZAR)") +
  theme_minimal()

ggsave(file.path(base,"visualisations","r_profit_by_category.png"),
       p2, width=9, height=5, dpi=150)
