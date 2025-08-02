"""Unit tests for configuration loading."""

import tempfile
from pathlib import Path

import yaml

from src.ai_media_monitor.core.config_loader import load_config
from src.ai_media_monitor.models import Config


class TestLoadConfig:
    """Tests for configuration loading."""

    def test_load_default_config(self, monkeypatch):
        """Test loading default configuration when no file exists."""
        # Change to a temporary directory where config.yaml doesn't exist
        with tempfile.TemporaryDirectory() as temp_dir:
            monkeypatch.chdir(temp_dir)
            config = load_config()

            assert isinstance(config, Config)
            assert "newspapers" in config.media_sources
            assert "trade_publications" in config.media_sources
            assert "tech_media" in config.media_sources
            assert "news_sites" in config.media_sources
            assert len(config.paywall_services) > 0
            assert config.retry_attempts == 3
            assert config.timeout == 30
            assert config.rate_limit == 10

    def test_load_config_from_file(self, monkeypatch):
        """Test loading configuration from YAML file."""
        config_data = {
            "media_sources": {
                "newspapers": [
                    {
                        "name": "Test Paper",
                        "url": "https://test.com",
                        "rss": "https://test.com/rss",
                        "categories": ["tech"],
                    }
                ]
            },
            "paywall_services": [
                {"url": "https://test-bypass.com", "method": "GET", "priority": 1}
            ],
            "retry_attempts": 5,
            "timeout": 45,
            "rate_limit": 15,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            monkeypatch.chdir(temp_dir)
            config_file = Path(temp_dir) / "config.yaml"

            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            config = load_config()

            assert isinstance(config, Config)
            assert len(config.media_sources["newspapers"]) == 1
            assert config.media_sources["newspapers"][0].name == "Test Paper"
            assert len(config.paywall_services) == 1
            assert config.paywall_services[0].url == "https://test-bypass.com"
            assert config.retry_attempts == 5
            assert config.timeout == 45
            assert config.rate_limit == 15

    def test_load_config_invalid_yaml(self, monkeypatch):
        """Test loading configuration with invalid YAML."""
        with tempfile.TemporaryDirectory() as temp_dir:
            monkeypatch.chdir(temp_dir)
            config_file = Path(temp_dir) / "config.yaml"

            # Write invalid YAML
            with open(config_file, "w") as f:
                f.write("invalid: yaml: content: [")

            # Should fall back to default config
            config = load_config()
            assert isinstance(config, Config)
            assert config.retry_attempts == 3  # Default value

    def test_load_config_invalid_structure(self, monkeypatch):
        """Test loading configuration with invalid structure."""
        config_data = {"invalid_field": "invalid_value", "missing_required_fields": True}

        with tempfile.TemporaryDirectory() as temp_dir:
            monkeypatch.chdir(temp_dir)
            config_file = Path(temp_dir) / "config.yaml"

            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Should fall back to default config due to validation error
            config = load_config()
            assert isinstance(config, Config)
            assert config.retry_attempts == 3  # Default value

    def test_default_config_structure(self):
        """Test that default configuration has expected structure."""
        # This tests the default config when no file exists
        with tempfile.TemporaryDirectory() as temp_dir:
            import os

            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                config = load_config()

                # Check media sources
                assert "newspapers" in config.media_sources
                assert "trade_publications" in config.media_sources
                assert "tech_media" in config.media_sources
                assert "news_sites" in config.media_sources

                # Check that each category has sources
                for _category, sources in config.media_sources.items():
                    assert len(sources) > 0
                    for source in sources:
                        assert source.name
                        assert source.url

                # Check paywall services
                assert len(config.paywall_services) > 0
                for service in config.paywall_services:
                    assert service.url
                    assert service.method in ["GET", "POST"]
                    assert isinstance(service.priority, int)

            finally:
                os.chdir(old_cwd)

    def test_specific_media_sources_in_default(self):
        """Test specific media sources in default configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            import os

            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                config = load_config()

                # Check for specific Dutch media sources
                newspaper_names = [source.name for source in config.media_sources["newspapers"]]
                assert "NRC" in newspaper_names
                assert "Volkskrant" in newspaper_names
                assert "FD" in newspaper_names

                tech_names = [source.name for source in config.media_sources["tech_media"]]
                assert "Tweakers" in tech_names
                assert "Bright" in tech_names

            finally:
                os.chdir(old_cwd)

    def test_paywall_services_in_default(self):
        """Test paywall services in default configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            import os

            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                config = load_config()

                service_urls = [service.url for service in config.paywall_services]
                assert "https://archive.ph" in service_urls
                assert "https://12ft.io" in service_urls

            finally:
                os.chdir(old_cwd)
