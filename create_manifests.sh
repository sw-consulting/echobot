#!/bin/bash
# Copyright (c) 2025 Maxim Samsonov  All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Usage: ./create_manifests.sh <base_tag>

base_tag=$1

# Registries configuration
declare -A registries=(
    ["ghcr"]="ghcr.io/sw.consulting"
)

# Create and push manifest for each registry
for registry_key in "${!registries[@]}"; do
    registry="${registries[$registry_key]}"
    echo "Creating manifest for ${registry}/echobot:${base_tag}"

    # Create manifest
    docker manifest create \
        "${registry}/echobot:${base_tag}" \
        --amend "${registry}/echobot:${base_tag}-amd64" \
        --amend "${registry}/echobot:${base_tag}-arm64"

    # Push manifest
    docker manifest push "${registry}/echobot:${base_tag}"

    # Handle latest tag for SHA tags
    if [[ $base_tag == sha* ]]; then
        echo "Creating latest manifest for ${registry}/echobot"
        docker manifest push "${registry}/echobot:${base_tag}"

        # Create and push latest tag
        docker manifest create \
            "${registry}/echobot:latest" \
            --amend "${registry}/echobot:${base_tag}-amd64" \
            --amend "${registry}/echobot:${base_tag}-arm64"

        docker manifest push "${registry}/echobot:latest"
    fi
done
