rm(list = ls(all.names = TRUE))

compute_test <- function(data, var_x, var_y, save_path, save_name_add = "", run_single = TRUE) {

  #####
  # Compute LME regression. The function fits an LME
  # with random intercepts for the 'var_y' and 'var_x' parameters.
  # The results of the model are saved in a file with the fit
  # coefficients and the p-values.
  #
  # Parameters:
  # data : data.frame
  #   dataframe containing patient, region and parameter data.
  # var_x : str
  #   name of the independent variable in data.
  # var_y : str
  #   name of the dependent variable in data.
  # save_path : str
  #   path where the csv files are saved.
  # save_name_add : str
  #   Additional string to append to the csv file names.
  # run_single : bool
  #   If True (Default), run regression for every sub-region.
  #
  # Returns:
  # df.test : dataframe with regression coefficients and p-values.
  #
  #####

  # Import package(s)
  library(nlme)
  library(MuMIn)

  # Levels of the "Region" factor
  Regions <- c("CTX", "ENT", "HIP", "AMY")

  a <- var_y

  # Format save name
  if (save_name_add != "") {
    save_name_add <- paste0("_", save_name_add)
  }

  # Convert columns to factors
  data$pat <- factor(data$pat)
  data$region <- factor(data$region, levels = Regions)

  ###
  # Run models
  ###

  # Store coefficients and significance
  m <- c()
  q <- c()
  rho <- c()
  statistics <- c()
  numdf <- c()
  dendf <- c()
  pval <- c()
  Group <- c("Overall")

  # LME - Random intercepts on all region
  LME.all <- lme(y ~ x,
    random = ~ 1 | pat, data = data,
    control = lmeControl(opt = "optim")
  )
  an <- anova.lme(LME.all)
  m[1] <- summary(LME.all)$coefficients$fixed[2]
  q[1] <- summary(LME.all)$coefficients$fixed[1]
  rho[1] <- sqrt(r.squaredGLMM(LME.all)[1]) * sign(m[1])
  statistics[1] <- an$`F-value`[2]
  numdf[1] <- an$`numDF`[2]
  dendf[1] <- an$`denDF`[2]
  pval[1] <- an$`p-value`[2]

  # LME - Random intercepts on single regions
  if (run_single == TRUE) {
    Group <- c(Group, Regions)
    for (i in 1:length(Regions)) {
      data.reg <- data[data$region == Regions[i], ]
      LME.reg <- lme(y ~ x,
        random = ~ 1 | pat, data = data.reg,
        control = lmeControl(opt = "optim")
      )
      an <- anova.lme(LME.reg)
      m[i + 1] <- summary(LME.reg)$coefficients$fixed[2]
      q[i + 1] <- summary(LME.reg)$coefficients$fixed[1]
      rho[i + 1] <- sqrt(r.squaredGLMM(LME.reg)[1]) * sign(m[i + 1])
      statistics[i + 1] <- an$`F-value`[2]
      numdf[i + 1] <- an$`numDF`[2]
      dendf[i + 1] <- an$`denDF`[2]
      pval[i + 1] <- min(an$`p-value`[2] * length(Regions), 1) # Bonferroni correction
    }
  }


  ###
  # Store and save data
  ###

  df.test <- data.frame(Group, m, q, rho, statistics, numdf, dendf, pval)
  rownames(df.test) <- NULL
  write.csv(df.test, paste0(save_path, "Test_corr_", var_x, "_", var_y, save_name_add, ".csv"))
  df.test
}
