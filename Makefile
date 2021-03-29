.EXPORT_ALL_VARIABLES:
PYTHONPATH = $(PWD)


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
	GoogleTuring/BackgroundTasks \
	FacebookCampaignsBuilder/BackgroundTasks


.PHONY: .all
all:
	# prevent running make without arguments from running the first target

.PHONY: test
test:
	$(foreach path,$(PROJECTS),$(MAKE) -C $(path) test;)

.PHONY: apps-local-start
apps-local-start:
	$(foreach path,$(PROJECTS),(nohup python3 $(path)/app.py 2>&1 >/dev/null &);)

.PHONY: apps-local-stop
apps-local-stop:
	$(foreach pid,$(shell pgrep -f Filed.Python),kill $(pid);)

.PHONY: apps-local-stop-brutal
apps-local-stop-brutal:
	$(foreach pid,$(shell pgrep -f Filed.Python),kill -9 $(pid);)

.PHONY: apps-local-list
apps-local-list:
	pgrep -af Filed.Python

.PHONY: clean
clean:
	$(foreach path,$(PROJECTS) .,rm -rf $(path)/logs;)
	find . -name '*.pyc' -delete
