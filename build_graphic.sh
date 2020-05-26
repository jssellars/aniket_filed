#!/bin/bash

# colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "=> ${GREEN}Checking environment...${NC}"

build='docker-compose build --force-rm'
push='docker-compose push'

command -v docker-compose >/dev/null 2>&1 || { echo -e >&2 "=>${RED}I require docker-compose but it's not installed.  Aborting.${NC}"; exit 1; }

echo -e "=> ${YELLOW}Setting initial .env for build - The default is DEV2...${NC}"

touch .env || exit
echo -e STAGE=dev2 > .env

function cleanup {
  echo -e "=> ${RED}Removing .env files...${NC}"
  rm  -rf .env .env-e
}

trap cleanup EXIT

declare -a services=(filed-ad-preview
                     filed-facebook-dexter-api
                     filed-facebook-turing-api
                     filed-potter-facebook-accounts-api
                     filed-potter-facebook-campaigns-builder-api
                     filed-potter-facebook-pixels-api
                     filed-targeting-search
                     filed-turing-api
                     filed-potter-facebook-accounts-background-tasks
                     filed-potter-facebook-audiences-background-tasks
                     filed-potter-facebook-pixels-background-tasks
                     filed-facebook-dexter-background-tasks
                     filed-facebook-turing-background-tasks
                     filed-potter-facebook-apps-background-tasks)


HEIGHT=20
WIDTH=80
CHOICE_HEIGHT=40
BACKTITLE="Docker images build script v0.1"
TITLE="Builder of docker containers"
MENU="Choose one of the following options:"

OPTIONS=(1 "=> Build DEV2 environment"
         2 "=> Build PROD environment"
         3 "=> Pull GIT sources"
         4 "=> Build specific DEV2 applications"
         4 "=> Build specific PROD applications")

while true; do

CHOICE=$(dialog --clear \
                --cancel-label "Exit" \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear

case $CHOICE in

        1)
            echo -e "=> ${GREEN}Build DEV2 environment${NC}"
            sed -i -e 's/STAGE=prod/STAGE=dev2/g' .env
            for image in "${services[@]}"
            do
            echo -e "=> ${YELLOW}Begin building of : ${image}${NC}"
            ${build} ${image}
            echo -e "=> ${GREEN} Done building ${image}${NC}"
            echo -e "=> ${GREEN} Pushing images to private repo...${NC}"
            ${push} ${image}
            echo -e "=> ${GREEN} Done pushing ${image}${NC}"
            done
            ;;
        2)
            echo -e "=> ${GREEN}Build PROD environment${NC}"
            sed -i -e 's/STAGE=dev2/STAGE=prod/g' .env
            for image in "${services[@]}"
            do
            echo -e "=> ${YELLOW}Begin building of : ${image}${NC}"
            ${build} ${image}
            echo -e "=> ${GREEN} Done building ${image}${NC}"
            echo -e "=> ${GREEN} Pushing images to private repo...${NC}"
            ${push} ${image}
            echo -e "=> ${GREEN} Done pushing ${image}${NC}"
            done
            ;;
        3)
            stage=$(\
            dialog --title "Pull repository branch" \
                    --cancel-label "Exit" \
                    --inputbox "Enter branch name:" 8 40 \
            3>&1 1>&2 2>&3 3>&- \
            )
            git pull origin "$stage"
            ;;
        4)
            sed -i -e 's/STAGE=prod/STAGE=dev2/g' .env
            pkglist=""
            n=1
            for pkg in ${services[@]}
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
                    ${build} ${choice}
                    echo -e "=> ${GREEN}Pushing images to private repo...${NC}"
                    ${push} ${choice}
                    done
            else
                    echo -e "=>${RED} Cancel selected ${NC}"
            fi
            break
            ;;            
        5)
            sed -i -e 's/STAGE=dev2/STAGE=prod/g' .env
            pkglist=""
            n=1
            for pkg in ${services[@]}
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
                    ${build} ${choice}
                    echo -e "=> ${GREEN}Pushing images to private repo...${NC}"
                    ${push} ${choice}
                    done
            else
                    echo -e "=>${RED} Cancel selected ${NC}"
            fi
            break
            ;; 
        "") 
            echo -e "=> ${GREEN}Execution done${NC}"
            break
            ;;                          
 esac
done 