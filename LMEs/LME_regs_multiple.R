rm(list = ls(all.names = TRUE))

compute_test <- function(data, save_path, save_name_add = "") {

  #####
  # Compute LME test on 'sequential' data.
  # The function fits an LME with random intercepts on each 'step'.
  # The results of the models are saved in two files with the fit
  # coefficients and the overall p-value at each step (with Bonferroni correction).
  # 
  # Parameters:
  # data : data.frame
  #   dataframe containing patient, region and parameter data.
  # save_path : str
  #   path where the csv files are saved.
  # save_name_add : str
  #   Additional string to append to the csv file names.
  #
  # Returns:
  # Results : list
  #   A list with two dataframes:
  #     - df.coef : LME fixed effects and SE for each step.
  #     - df.test : p-values for overall significance.
  #####

  # Import package(s)
  library(nlme)

  # Levels of the "Region" factor
  Regions <- c("CTX", "ENT", "HIP", "AMY")

  # Format save name
  if (save_name_add != "") {
    save_name_add <- paste0("_", save_name_add)
  }

  # Keep needed columns
  keeps <- c("pat", "region", names(data)[5:length(names(data))])
  data <- data[keeps]

  # Convert columns to factors
  data$pat <- factor(data$pat)
  data$region <- factor(data$region, levels = Regions)

  # Total number of steps
  N <- ncol(data) - 2

  # Steps
  steps <- as.numeric(names(data)[3:length(names(data))])

  # Rename columns
  colnames(data) <- c("pat", "region", paste("X", seq(N), sep = ""))

  ###
  # Run models
  ###

  # Create empty vector to store p-values
  df.coef <- setNames(
    data.frame(matrix(ncol = 8, nrow = 0)),
    c(paste(Regions, "mean", sep = "_"), paste(Regions, "sem", sep = "_"))
  )
  pval <- c()



  # Run a model for every step
  for (i in 1:N) {
    LME_st <- lme(formula(paste0("X", as.character(i), "~ region")),
      random = ~ 1 | pat,
      data = data, control = lmeControl(opt = "optim")
    )
    # Significance test
    an <- anova.lme(LME_st)
    pval[i] <- an$`p-value`[2] * N # Bonferroni correction
    # Access model summary
    mod.sum <- summary(LME_st)
    # Fixed effects
    means <- mod.sum$coefficients$fixed
    # Re-add intercept term
    means[-1] <- means[-1] + means[1]
    # Standard Errors
    sems <- sqrt(diag(mod.sum$varFix))
    # Add to coefficients
    df.coef[i, ] <- c(as.numeric(means), as.numeric(sems))
  }

  # Write test results to dataframe
  df.test <- data.frame(steps, pval)

  # Save
  write.csv(df.coef, paste0(save_path, "Test_coef", save_name_add, ".csv"))
  write.csv(df.test, paste0(save_path, "Test_pval", save_name_add, ".csv"))

  # Return both dataframes as list
  Results <- list("Coef" = df.coef, "Test" = df.test)
}
