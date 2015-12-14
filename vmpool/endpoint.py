# coding: utf-8

from core.utils import generator_wait_for
from core.logger import log_pool
from core.config import config

from core.exceptions import PlatformException, CreationException
from vmpool.platforms import Platforms

from flask import current_app


def get_platform(desired_caps):
    platform = desired_caps.get('platform', None)

    if hasattr(config, "PLATFORM") and config.PLATFORM:
        log_pool.info(
            'Using %s. Desired platform %s has been ignored.' %
            (config.PLATFORM, platform)
        )
        platform = config.PLATFORM
        desired_caps["platform"] = platform

    if isinstance(platform, unicode):
        platform = platform.encode('utf-8')

    if not platform:
        raise CreationException(
            'Platform parameter for new endpoint not found in dc'
        )

    if not Platforms.check_platform(platform):
        raise PlatformException('No such platform %s' % platform)

    return platform


def get_vm(desired_caps):
    platform = get_platform(desired_caps)

    vm = None
    for _ in generator_wait_for(
        lambda: vm, timeout=config.GET_VM_TIMEOUT
    ):
        vm = current_app.pool.get_vm(platform)
        if vm:
            break

    if not vm:
        raise CreationException(
            "Timeout while waiting for vm with platform %s" % platform
        )

    yield vm

    for _ in generator_wait_for(
        lambda: vm.ready, timeout=config.GET_VM_TIMEOUT
    ):
        yield vm

    if not vm.ready:
        raise CreationException(
            'Timeout while building vm %s (platform: %s)' %
            (vm.name, platform)
        )

    log_pool.info('Got vm for request with params: %s' % vm.info)
    yield vm
