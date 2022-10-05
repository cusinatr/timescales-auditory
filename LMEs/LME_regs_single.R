rm(list = ls(all.names = TRUE))

compute_test <- function(data, var, save_path, save_name_add = "") {

  #####
  # Compute LME test on 'categorical' data with 'region' factor.
  # The function fits an LME with random intercepts for the 'var' parameter.
  # The results of the model are saved in two files with the fit
  # coefficients and the p-values of each comparison.
  #
  # Parameters:
  # data : data.frame
  #   dataframe containing patient, region and parameter data.
  # var : str
  #   name of the variable of interest in data.
  # save_path : str
  #   path where the csv files are saved.
  # save_name_add : str
  #   Additional string to append to the csv file names.
  #
  # Returns:
  # Results : list
  #   A list with two dataframes:
  #     - df.coef : LME fixed effects and SE for each level.
  #     - df.test : p-values for overall significance and pairwise comparisons.
  #####

  # Import package(s)
  library(nlme)
  library(emmeans)

  # Levels of the "Region" factor
  Regions <- c("CTX", "ENT", "HIP", "AMY")

  # Format save name
  if (save_name_add != "") {
    save_name_add <- paste0("_", save_name_add)
  }

  # Keep needed columns
  keeps <- c("pat", "region", var)
  data <- data[keeps]

  # Convert columns to factors
  data$pat <- factor(data$pat)
  data$region <- factor(data$region, levels = Regions)

  ###
  # Run model
  ###

  # LME - Random intercepts
  LME <- lme(formula(paste0(var, "~ region")),
    random = ~ 1 | pat, data = data,
    control = lmeControl(opt = "optim")
  )

  ###
  # Extract average values per category
  ###

  # Access model summary
  mod.sum <- summary(LME)

  # Fixed effects
  Coef <- mod.sum$coefficients$fixed
  # Re-add intercept term
  Coef[-1] <- Coef[-1] + Coef[1]

  # Standard Errors
  SE <- sqrt(diag(mod.sum$varFix))

  # Create dataframe
  df.coef <- data.frame(Regions, Coef, SE)
  rownames(df.coef) <- NULL
  # Save
  write.csv(df.coef, paste0(save_path, "Test_coef_", var, save_name_add, ".csv"))

  ###
  # Extract test statistics
  ###

  # Overall p-value
  an <- anova.lme(LME)

  # Pairwise contrasts
  pairs <- pairs(emmeans(LME, specs = "region"))

  # Create dataframe
  Comparisons <- c("Overall", unlist(pairs@levels))
  statistics <- c(an$`F-value`[2], summary(pairs)$t.ratio)
  numdf <- c(an$`numDF`[2], summary(pairs)$df)
  dendf <- c(an$`denDF`[2], rep(0, length(summary(pairs)$df)))
  pvalue <- c(an$`p-value`[2], summary(pairs)$p.value)
  df.test <- data.frame(Comparisons, statistics, numdf, dendf, pvalue)
  rownames(df.test) <- NULL
  # Save
  write.csv(df.test, paste0(save_path, "Test_pval_", var, save_name_add, ".csv"))

  # Return both dataframes as list
  Results <- list("Coef" = df.coef, "Test" = df.test)
}
