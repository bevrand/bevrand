#!/usr/bin/env bash

kubectl delete -n default deploy,svc,cm,secret,sts,serviceaccount,ingress,role,rolebinding --all
