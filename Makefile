PROJECTS := \
	FacebookAccounts/Api \
	FacebookCampaignsBuilder/Api \
	FacebookDexter/Api \
	FacebookPixels/Api \
	FacebookTuring/Api \
	GoogleTuring/Api \
	Logging/Api \
	FacebookAccounts/BackgroundTasks \
	FacebookApps/BackgroundTasks \
	FacebookAudiences/BackgroundTasks \
	FacebookDexter/BackgroundTasks \
	FacebookPixels/BackgroundTasks \
	FacebookProductCatalogs/BackgroundTasks \
	FacebookTuring/BackgroundTasks \
	GoogleDexter/BackgroundTasks \
	GoogleTuring/BackgroundTasks

.PHONY: .all
all:
	# prevent running make without arguments from running the first target

.PHONY: test
test:
	$(foreach path,$(PROJECTS),$(MAKE) -C $(path) test;)

.PHONY: clean
clean:
	$(foreach path,$(PROJECTS),rm -rf $(path)/logs;)
	find . -name '*.pyc' -delete
