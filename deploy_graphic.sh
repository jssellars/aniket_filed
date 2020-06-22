#!/bin/bash

# colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

command -v kubectl >/dev/null 2>&1 || { echo -e >&2 "=>${RED}I require kubectl but it's not installed.  Aborting.${NC}"; exit 1; }

declare -a services_api=(filed-ad-preview
                         filed-facebook-dexter-api
                         filed-facebook-turing-api
                         filed-potter-facebook-accounts-api
                         filed-potter-facebook-campaigns-builder-api
                         filed-potter-facebook-pixels-api
                         filed-targeting-search
                         filed-facebook-turing-api)

declare -a services_tasks=(filed-potter-facebook-accounts-background-tasks
                           filed-potter-facebook-apps-background-tasks
                           filed-potter-facebook-audiences-background-tasks
                           filed-potter-facebook-pixels-background-tasks
                           filed-facebook-dexter-background-tasks
                           filed-facebook-turing-background-tasks)

HEIGHT=20
WIDTH=100
CHOICE_HEIGHT=40
BACKTITLE="Kubernetes deployment script v0.1"
TITLE="Deployment for kubernetes services"
MENU="Choose one of the following options:"

OPTIONS=(1 "=> Deploy DEV2 environment API"
         2 "=> Deploy DEV2 environment TASKS"
         3 "=> Deploy PROD environment API"
         4 "=> Deploy PROD environment TASKS"
         5 "=> Deploy DEV2 environment SERVICES - Load Balancers WILL be modified !!"
         6 "=> Deploy PROD environment SERVICES - Load Balancers WILL be modified !!"         
         7 "=> Deploy specific DEV2 POD's - API"
         8 "=> Deploy specific DEV2 POD's - TASKS"
         9 "=> Deploy specific PROD POD's - API"
         10 "=> Deploy specific PROD POD's - TASKS")


CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear



case $CHOICE in
        1)
            echo -e "=> ${GREEN}Deploy DEV2 environment API${NC}"
            for api in "${services_api[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment of : ${api}${NC}"
            echo -e  "=> ${RED}Deleting previous deployment...${NC}"
            kubectl delete -f Kube_Deploy/${api}/dev2/api.yaml
            echo -e  "=> ${YELLOW}Apply new deployment...${NC}"
            kubectl apply -f Kube_Deploy/${api}/dev2/api.yaml
            echo -e  "=> ${GREEN}DEV2 environment deployment completed ! Check for errors...${NC}"
            done
            ;;
        2)
            echo -e "=> ${GREEN}Deploy DEV2 environment TASKS${NC}"
            for tasks in "${services_tasks[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment of : ${tasks}${NC}"
            echo -e  "=> ${RED}Deleting previous deployment...${NC}"
            kubectl delete -f Kube_Deploy/${tasks}/dev2/tasks.yaml
            echo -e  "=> ${YELLOW}Apply new deployment...${NC}"
            kubectl apply -f Kube_Deploy/${tasks}/dev2/tasks.yaml
            echo -e  "=> ${GREEN}DEV2 environment deployment completed ! Check for errors...${NC}"
            done
            ;;
        3)
            echo -e "=> ${GREEN}Deploy PROD environment API${NC}"
            for api in "${services_api[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment of : ${api}${NC}"
            echo -e  "=> ${RED}Deleting previous deployment...${NC}"
            kubectl delete -f Kube_Deploy/${api}/prod/api.yaml
            echo -e  "=> ${YELLOW}Apply new deployment...${NC}"
            kubectl apply -f Kube_Deploy/${api}/prod/api.yaml
            echo -e  "=> ${GREEN}PROD environment deployment completed ! Check for errors...${NC}"
            done
            ;;
        4)
            echo -e "=> ${GREEN}Deploy PROD environment TASKS${NC}"
            for tasks in "${services_tasks[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment of : ${api}${NC}"
            echo -e  "=> ${RED}Deleting previous deployment...${NC}"
            kubectl delete -f Kube_Deploy/${tasks}/prod/api.yaml
            echo -e  "=> ${YELLOW}Apply new deployment...${NC}"
            kubectl apply -f Kube_Deploy/${tasks}/prod/api.yaml
            echo -e  "=> ${GREEN}PROD environment deployment completed ! Check for errors...${NC}"
            done
            ;;
        5)
            # Api below
            echo -e "=> ${GREEN}Deploy DEV2 environment SERVICES${NC}"
            for api in "${services_api[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment service apply of : ${api}${NC}"
            echo -e  "=> ${YELLOW}Apply new service...${NC}"
            kubectl apply -f Kube_Deploy/${api}/dev2/service.yaml
            echo -e  "=> ${GREEN}DEV2 service deployment completed ! Check for errors...${NC}"
            done
            # Background Tasks below
            for tasks in "${services_tasks[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment service apply of : ${api}${NC}"
            echo -e  "=> ${YELLOW}Apply new service...${NC}"
            kubectl apply -f Kube_Deploy/${tasks}/dev2/service.yaml
            echo -e  "=> ${GREEN}DEV2 service deployment completed ! Check for errors...${NC}"
            done
            ;;
        6)
            # Api below
            echo -e "=> ${GREEN}Deploy PROD environment SERVICES${NC}"
            for api in "${services_api[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment service apply of : ${api}${NC}"
            echo -e  "=> ${YELLOW}Apply new service...${NC}"
            kubectl apply -f Kube_Deploy/${api}/prod/service.yaml
            echo -e  "=> ${GREEN}PROD service deployment completed ! Check for errors...${NC}"
            done
            # Background Tasks below
            for tasks in "${services_tasks[@]}"
            do
            echo -e  "=> ${GREEN}Begin deployment service apply of : ${api}${NC}"
            echo -e  "=> ${YELLOW}Apply new service...${NC}"
            kubectl apply -f Kube_Deploy/${tasks}/prod/service.yaml
            echo -e  "=> ${GREEN}PROD service deployment completed ! Check for errors...${NC}"
            done
            ;;            
        7)
            pkglist=""
            n=1
            for pkg in ${services_api[@]}
            do
                    pkglist="$pkglist $pkg $n off"
                    n=$[n+1]
            done

            choices=`dialog --stdout --cancel-label "Exit" --checklist 'Choose item:' 40 80 60 $pkglist`

            if [ $? -eq 0 ]
            then
                    for choice in $choices
                    do
                    echo -e "=> ${YELLOW}Begin building of : ${choice}${NC}"
                    echo -e  "=> ${GREEN}Begin deployment of : ${tasks}${NC}"
                    echo -e  "=> ${RED}Deleting previous deployment...${NC}"
                    kubectl delete -f Kube_Deploy/${choice}/dev2/api.yaml
                    echo -e  "=> ${YELLOW}Apply new deployment...${NC}"
                    kubectl apply -f Kube_Deploy/${choice}/dev2/api.yaml
                    echo -e  "=> ${GREEN}DEV2 selected API POD's deployed ! Check for errors...${NC}"
                    done
            else
                    echo -e "=>${RED} Cancel selected ${NC}"
            fi
            ;;
        8)
            pkglist=""
            n=1
            for pkg in ${services_tasks[@]}
            do
                    pkglist="$pkglist $pkg $n off"
                    n=$[n+1]
            done

            choices=`dialog --stdout --cancel-label "Exit" --checklist 'Choose item:' 40 80 60 $pkglist`

            if [ $? -eq 0 ]
            then
                    for choice in $choices
                    do
                    echo -e "=> ${YELLOW}Begin building of : ${choice}${NC}"
                    echo -e  "=> ${GREEN}Begin deployment of : ${tasks}${NC}"
                    echo -e  "=> ${RED}Deleting previous deployment...${NC}"
                    kubectl delete -f Kube_Deploy/${choice}/dev2/tasks.yaml
                    echo -e  "=> ${YELLOW}Apply new deployment...${NC}"
                    kubectl apply -f Kube_Deploy/${choice}/dev2/tasks.yaml
                    echo -e  "=> ${GREEN}DEV2 selected API POD's deployed ! Check for errors...${NC}"
                    done
            else
                    echo -e "=>${RED} Cancel selected ${NC}"
            fi      
            ;;
esac