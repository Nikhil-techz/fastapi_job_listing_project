import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ArrowRight,
  BriefcaseBusiness,
  Building2,
  Check,
  CircleDollarSign,
  Edit3,
  LogIn,
  LogOut,
  MapPin,
  Plus,
  RefreshCw,
  Search,
  Trash2,
  UserPlus,
  Users,
  X,
} from 'lucide-react';
import employerHero from './assets/employer-hero.png';
import './styles.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const blankAuth = {
  name: '',
  email: '',
  password: '',
  role: 'applicant',
};

const blankJob = {
  title: '',
  company: '',
  location: '',
  salary: '',
  experience_level: '',
  skills: '',
  description: '',
};

function App() {
  const [audience, setAudience] = useState('seeker');
  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [authMode, setAuthMode] = useState('login');
  const [authForm, setAuthForm] = useState(blankAuth);
  const [jobForm, setJobForm] = useState(blankJob);
  const [editingJobId, setEditingJobId] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('job_api_token') || '');
  const [profile, setProfile] = useState(null);
  const [query, setQuery] = useState('');
  const [locationQuery, setLocationQuery] = useState('');
  const [status, setStatus] = useState({ type: 'idle', message: '' });
  const [loading, setLoading] = useState(false);
  const [authSubmitting, setAuthSubmitting] = useState(false);

  const selectedJob = jobs.find((job) => job.id === selectedJobId) || jobs[0] || null;
  const isRecruiter = profile?.role === 'recruiter';
  const isLoggedIn = Boolean(profile);

  const filteredJobs = useMemo(() => {
    const text = query.trim().toLowerCase();
    const place = locationQuery.trim().toLowerCase();

    return jobs.filter((job) => {
      const matchesText =
        !text ||
        [job.title, job.company, job.skills, job.description]
          .filter(Boolean)
          .some((value) => value.toLowerCase().includes(text));
      const matchesLocation = !place || job.location?.toLowerCase().includes(place);
      return matchesText && matchesLocation;
    });
  }, [jobs, query, locationQuery]);

  useEffect(() => {
    loadJobs();
  }, []);

  useEffect(() => {
    setAuthForm((current) => ({
      ...current,
      role: audience === 'employer' ? 'recruiter' : 'applicant',
    }));
  }, [audience]);

  useEffect(() => {
    if (token) {
      localStorage.setItem('job_api_token', token);
      loadProfile(token);
    } else {
      localStorage.removeItem('job_api_token');
      setProfile(null);
    }
  }, [token]);

  async function request(path, options = {}) {
    let response;

    try {
      response = await fetch(`${API_BASE_URL}${path}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
          ...options.headers,
        },
      });
    } catch (error) {
      throw new Error(`Cannot connect to FastAPI at ${API_BASE_URL}. Start the backend and refresh.`);
    }

    const contentType = response.headers.get('content-type') || '';
    const payload = contentType.includes('application/json') ? await response.json() : null;

    if (!response.ok) {
      throw new Error(payload?.detail || 'Something went wrong');
    }

    return payload;
  }

  async function loadJobs() {
    setLoading(true);
    try {
      const data = await request('/jobs/');
      setJobs(data);
      setSelectedJobId((current) => current || data[0]?.id || null);
    } catch (error) {
      setStatus({ type: 'error', message: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function loadProfile(activeToken = token) {
    try {
      let response;

      try {
        response = await fetch(`${API_BASE_URL}/auth/profile`, {
          headers: { Authorization: `Bearer ${activeToken}` },
        });
      } catch (error) {
        throw new Error(`Cannot connect to FastAPI at ${API_BASE_URL}. Start the backend and refresh.`);
      }

      const payload = await response.json();
      if (!response.ok) throw new Error(payload?.detail || 'Session expired');
      setProfile(payload);
      setAudience(payload.role === 'recruiter' ? 'employer' : 'seeker');
    } catch (error) {
      setToken('');
      setStatus({ type: 'error', message: error.message });
    }
  }

  async function handleAuth(event) {
    event.preventDefault();
    setStatus({ type: 'idle', message: '' });
    setAuthSubmitting(true);

    try {
      const activeRole = audience === 'employer' ? 'recruiter' : 'applicant';

      if (authMode === 'register') {
        await request('/users/register', {
          method: 'POST',
          body: JSON.stringify({
            name: authForm.name,
            email: authForm.email,
            password: authForm.password,
            role: activeRole,
          }),
        });

        const data = await request('/auth/login', {
          method: 'POST',
          body: JSON.stringify({
            email: authForm.email,
            password: authForm.password,
          }),
        });
        setToken(data.access_token);
        setAuthForm({ ...blankAuth, role: activeRole });
        setStatus({ type: 'success', message: 'Account created and logged in successfully.' });
        return;
      }

      const data = await request('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          email: authForm.email,
          password: authForm.password,
        }),
      });
      setToken(data.access_token);
      setAuthForm(blankAuth);
      setStatus({ type: 'success', message: 'Logged in successfully.' });
    } catch (error) {
      setStatus({ type: 'error', message: error.message });
    } finally {
      setAuthSubmitting(false);
    }
  }

  function handleLogout() {
    setToken('');
    setProfile(null);
    setStatus({ type: 'success', message: 'Logged out successfully.' });
  }

  async function handleSaveJob(event) {
    event.preventDefault();
    const payload = {
      ...jobForm,
      salary: Number(jobForm.salary),
      experience_level: Number(jobForm.experience_level),
    };

    try {
      const path = editingJobId ? `/jobs/${editingJobId}` : '/jobs/';
      await request(path, {
        method: editingJobId ? 'PUT' : 'POST',
        body: JSON.stringify(payload),
      });
      setStatus({
        type: 'success',
        message: editingJobId ? 'Job updated successfully.' : 'Job posted successfully.',
      });
      setJobForm(blankJob);
      setEditingJobId(null);
      await loadJobs();
    } catch (error) {
      setStatus({ type: 'error', message: error.message });
    }
  }

  async function handleDeleteJob(jobId) {
    try {
      await request(`/jobs/${jobId}`, { method: 'DELETE' });
      setStatus({ type: 'success', message: 'Job deleted successfully.' });
      setSelectedJobId(null);
      await loadJobs();
    } catch (error) {
      setStatus({ type: 'error', message: error.message });
    }
  }

  function startEdit(job) {
    setAudience('employer');
    setEditingJobId(job.id);
    setJobForm({
      title: job.title,
      company: job.company,
      location: job.location,
      salary: job.salary,
      experience_level: job.experience_level,
      skills: job.skills,
      description: job.description,
    });
  }

  function openRegister(targetAudience) {
    setAudience(targetAudience);
    setAuthMode('register');
    setAuthForm({
      ...blankAuth,
      role: targetAudience === 'employer' ? 'recruiter' : 'applicant',
    });
  }

  return (
    <main className={`site-shell ${audience}`}>
      <header className="site-header">
        <button className="brand" onClick={() => setAudience('seeker')}>
          <span className="brand-mark">J</span>
          <span>JobSphere</span>
        </button>

        <nav className="audience-tabs" aria-label="Audience">
          <button className={audience === 'seeker' ? 'active' : ''} onClick={() => setAudience('seeker')}>
            Job Seekers
          </button>
          <button
            className={audience === 'employer' ? 'active' : ''}
            onClick={() => setAudience('employer')}
          >
            Employers
          </button>
        </nav>

        <div className="header-actions">
          {profile ? (
            <div className="session-pill">
              <span>{profile.name || profile.email}</span>
              <strong>{profile.role}</strong>
              <button onClick={handleLogout} title="Logout">
                <LogOut size={18} />
              </button>
            </div>
          ) : (
            <button className="text-button" onClick={() => setAuthMode('login')}>
              Sign in
            </button>
          )}
          <button className="header-cta" onClick={() => setAudience('employer')}>
            Post a job
          </button>
        </div>
      </header>

      {status.message && (
        <div className={`notice ${status.type}`}>
          <span>{status.message}</span>
          <button onClick={() => setStatus({ type: 'idle', message: '' })} title="Dismiss">
            <X size={16} />
          </button>
        </div>
      )}

      {audience === 'seeker' ? (
        <JobSeekerView
          authForm={authForm}
          authMode={authMode}
          authSubmitting={authSubmitting}
          filteredJobs={filteredJobs}
          isLoggedIn={isLoggedIn}
          isRecruiter={isRecruiter}
          loading={loading}
          locationQuery={locationQuery}
          onAuth={handleAuth}
          onDeleteJob={handleDeleteJob}
          onEditJob={startEdit}
          onLoadJobs={loadJobs}
          onOpenRegister={() => openRegister('seeker')}
          onSelectJob={setSelectedJobId}
          query={query}
          selectedJob={selectedJob}
          setAuthForm={setAuthForm}
          setAuthMode={setAuthMode}
          setLocationQuery={setLocationQuery}
          setQuery={setQuery}
          status={status}
        />
      ) : (
        <EmployerView
          authForm={authForm}
          authMode={authMode}
          authSubmitting={authSubmitting}
          editingJobId={editingJobId}
          isRecruiter={isRecruiter}
          jobForm={jobForm}
          jobs={jobs}
          onAuth={handleAuth}
          onCancelEdit={() => {
            setEditingJobId(null);
            setJobForm(blankJob);
          }}
          onDeleteJob={handleDeleteJob}
          onEditJob={startEdit}
          onOpenRegister={() => openRegister('employer')}
          onSaveJob={handleSaveJob}
          profile={profile}
          setAuthForm={setAuthForm}
          setAuthMode={setAuthMode}
          setJobForm={setJobForm}
          status={status}
        />
      )}
    </main>
  );
}

function JobSeekerView({
  authForm,
  authMode,
  authSubmitting,
  filteredJobs,
  isLoggedIn,
  isRecruiter,
  loading,
  locationQuery,
  onAuth,
  onDeleteJob,
  onEditJob,
  onLoadJobs,
  onOpenRegister,
  onSelectJob,
  query,
  selectedJob,
  setAuthForm,
  setAuthMode,
  setLocationQuery,
  setQuery,
  status,
}) {
  const [searchSubmitting, setSearchSubmitting] = useState(false);

  async function handleSearch(event) {
    event.preventDefault();
    setSearchSubmitting(true);

    try {
      await Promise.all([
        onLoadJobs(),
        new Promise((resolve) => setTimeout(resolve, 600)),
      ]);
    } finally {
      setSearchSubmitting(false);
    }
  }

  const isSearching = loading || searchSubmitting;

  return (
    <>
      <section className="seeker-hero">
        <form className={`job-search-bar ${isSearching ? 'searching' : ''}`} onSubmit={handleSearch}>
          <label>
            <Search size={24} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Job title, keywords, or company"
            />
          </label>
          <span className="divider" />
          <label>
            <MapPin size={24} />
            <input
              value={locationQuery}
              onChange={(event) => setLocationQuery(event.target.value)}
              placeholder="City, state, or remote"
            />
          </label>
          <button type="submit" disabled={isSearching} aria-busy={isSearching}>
            {isSearching ? <RefreshCw size={20} className="spin" /> : <Search size={20} />}
            {isSearching ? 'Searching...' : 'Find jobs'}
          </button>
        </form>

        <div className="seeker-title">
          <div className="wordmark">JobSphere</div>
          <h1>Your next job starts here</h1>
          <p>Create an account or sign in to see jobs that match your profile.</p>
          {!isLoggedIn && (
            <button className="primary-button hero-button" onClick={onOpenRegister}>
              Get Started
              <ArrowRight size={20} />
            </button>
          )}
        </div>
      </section>

      <section className="content-grid seeker-grid">
        {!isLoggedIn && (
          <AuthPanel
            authForm={authForm}
            authMode={authMode}
            authSubmitting={authSubmitting}
            fixedRole="applicant"
            onAuth={onAuth}
            setAuthForm={setAuthForm}
            setAuthMode={setAuthMode}
            status={status}
            title="Job seeker account"
          />
        )}

        <section className="job-board">
          <div className="section-head">
            <div>
              <p className="eyebrow">Available roles</p>
              <h2>{filteredJobs.length} jobs found</h2>
            </div>
            <button className="icon-button" onClick={onLoadJobs} title="Refresh jobs">
              <RefreshCw size={18} className={loading ? 'spin' : ''} />
            </button>
          </div>

          <div className="jobs-grid">
            <div className="job-list">
              {filteredJobs.map((job) => (
                <button
                  key={job.id}
                  className={`job-card ${selectedJob?.id === job.id ? 'selected' : ''}`}
                  onClick={() => onSelectJob(job.id)}
                >
                  <span className="job-title">{job.title}</span>
                  <span className="meta">
                    <Building2 size={15} />
                    {job.company}
                  </span>
                  <span className="meta">
                    <MapPin size={15} />
                    {job.location}
                  </span>
                </button>
              ))}

              {!filteredJobs.length && <div className="empty-state">No jobs found.</div>}
            </div>

            <JobDetails
              isRecruiter={isRecruiter}
              job={selectedJob}
              onDeleteJob={onDeleteJob}
              onEditJob={onEditJob}
            />
          </div>
        </section>
      </section>
    </>
  );
}

function EmployerView({
  authForm,
  authMode,
  authSubmitting,
  editingJobId,
  isRecruiter,
  jobForm,
  jobs,
  onAuth,
  onCancelEdit,
  onDeleteJob,
  onEditJob,
  onOpenRegister,
  onSaveJob,
  profile,
  setAuthForm,
  setAuthMode,
  setJobForm,
  status,
}) {
  return (
    <>
      <section className="employer-hero">
        <div className="employer-copy">
          <p className="eyebrow">JobSphere for employers</p>
          <h1>Let's hire your next great candidate. Fast.</h1>
          <p>No matter the skills, experience, or qualifications you need, post roles and manage them here.</p>
          <button className="warm-button" onClick={isRecruiter ? undefined : onOpenRegister}>
            Post a job
          </button>
        </div>
        <img src={employerHero} alt="Professional reviewing candidates on a laptop" />
      </section>

      <section className="content-grid employer-grid">
        {!profile && (
          <AuthPanel
            authForm={authForm}
            authMode={authMode}
            authSubmitting={authSubmitting}
            fixedRole="recruiter"
            onAuth={onAuth}
            setAuthForm={setAuthForm}
            setAuthMode={setAuthMode}
            status={status}
            title="Employer account"
          />
        )}

        {profile && !isRecruiter && (
          <div className="panel locked-panel">
            <Users size={30} />
            <h2>Recruiter account required</h2>
            <p>You are signed in as an applicant. Create or login with a recruiter account to post jobs.</p>
          </div>
        )}

        {isRecruiter && (
          <PostJobPanel
            editingJobId={editingJobId}
            jobForm={jobForm}
            onCancelEdit={onCancelEdit}
            onSaveJob={onSaveJob}
            setJobForm={setJobForm}
          />
        )}

        <section className="job-board employer-jobs">
          <div className="section-head">
            <div>
              <p className="eyebrow">Current listings</p>
              <h2>{jobs.length} active jobs</h2>
            </div>
          </div>

          <div className="employer-list">
            {jobs.map((job) => (
              <article className="employer-job-card" key={job.id}>
                <div>
                  <h3>{job.title}</h3>
                  <p>{job.company} - {job.location}</p>
                </div>
                {isRecruiter && (
                  <div className="actions compact-actions">
                    <button onClick={() => onEditJob(job)}>
                      <Edit3 size={16} />
                      Edit
                    </button>
                    <button className="danger" onClick={() => onDeleteJob(job.id)}>
                      <Trash2 size={16} />
                      Delete
                    </button>
                  </div>
                )}
              </article>
            ))}
          </div>
        </section>
      </section>
    </>
  );
}

function AuthPanel({
  authForm,
  authMode,
  authSubmitting,
  fixedRole,
  onAuth,
  setAuthForm,
  setAuthMode,
  status,
  title,
}) {
  const roleLabel = fixedRole === 'recruiter' ? 'Recruiter' : 'Applicant';

  return (
    <aside className="panel auth-panel">
      <div className="panel-heading">
        <h2>{title}</h2>
        <span>{roleLabel}</span>
      </div>
      <div className="tabs">
        <button className={authMode === 'login' ? 'active' : ''} onClick={() => setAuthMode('login')}>
          <LogIn size={16} />
          Login
        </button>
        <button className={authMode === 'register' ? 'active' : ''} onClick={() => setAuthMode('register')}>
          <UserPlus size={16} />
          Register
        </button>
      </div>

      {status.message && <div className={`inline-notice ${status.type}`}>{status.message}</div>}

      <form onSubmit={onAuth} className="stack">
        {authMode === 'register' && (
          <label>
            Name
            <input
              value={authForm.name}
              onChange={(event) => setAuthForm({ ...authForm, name: event.target.value, role: fixedRole })}
              required
            />
          </label>
        )}
        <label>
          Email
          <input
            type="email"
            value={authForm.email}
            onChange={(event) => setAuthForm({ ...authForm, email: event.target.value, role: fixedRole })}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={authForm.password}
            onChange={(event) => setAuthForm({ ...authForm, password: event.target.value, role: fixedRole })}
            required
          />
        </label>
        <input type="hidden" value={fixedRole} readOnly />
        <button className="primary-button" type="submit" disabled={authSubmitting}>
          {authMode === 'login' ? <LogIn size={18} /> : <UserPlus size={18} />}
          {authSubmitting
            ? authMode === 'login'
              ? 'Logging in...'
              : 'Creating account...'
            : authMode === 'login'
              ? 'Login'
              : `Create ${roleLabel.toLowerCase()} account`}
        </button>
      </form>
    </aside>
  );
}

function PostJobPanel({ editingJobId, jobForm, onCancelEdit, onSaveJob, setJobForm }) {
  return (
    <aside className="panel post-panel">
      <div className="form-title">
        <h2>{editingJobId ? 'Edit job' : 'Post a job'}</h2>
        {editingJobId && (
          <button className="icon-button" onClick={onCancelEdit} title="Cancel edit">
            <X size={18} />
          </button>
        )}
      </div>
      <form className="stack" onSubmit={onSaveJob}>
        <label>
          Title
          <input
            value={jobForm.title}
            onChange={(event) => setJobForm({ ...jobForm, title: event.target.value })}
            required
          />
        </label>
        <label>
          Company
          <input
            value={jobForm.company}
            onChange={(event) => setJobForm({ ...jobForm, company: event.target.value })}
            required
          />
        </label>
        <label>
          Location
          <input
            value={jobForm.location}
            onChange={(event) => setJobForm({ ...jobForm, location: event.target.value })}
            required
          />
        </label>
        <div className="two-columns">
          <label>
            Salary
            <input
              type="number"
              value={jobForm.salary}
              onChange={(event) => setJobForm({ ...jobForm, salary: event.target.value })}
              required
            />
          </label>
          <label>
            Experience
            <input
              type="number"
              value={jobForm.experience_level}
              onChange={(event) => setJobForm({ ...jobForm, experience_level: event.target.value })}
              required
            />
          </label>
        </div>
        <label>
          Skills
          <input
            value={jobForm.skills}
            onChange={(event) => setJobForm({ ...jobForm, skills: event.target.value })}
            required
          />
        </label>
        <label>
          Description
          <textarea
            value={jobForm.description}
            onChange={(event) => setJobForm({ ...jobForm, description: event.target.value })}
            required
          />
        </label>
        <button className="primary-button" type="submit">
          <Plus size={18} />
          {editingJobId ? 'Update job' : 'Post job'}
        </button>
      </form>
    </aside>
  );
}

function JobDetails({ isRecruiter, job, onDeleteJob, onEditJob }) {
  if (!job) {
    return <div className="detail-panel empty-state">Select a job to see details.</div>;
  }

  return (
    <article className="detail-panel">
      <div className="detail-head">
        <div>
          <p className="eyebrow">{job.company}</p>
          <h2>{job.title}</h2>
        </div>
        <BriefcaseBusiness size={26} />
      </div>

      <div className="facts">
        <span>
          <MapPin size={16} />
          {job.location}
        </span>
        <span>
          <CircleDollarSign size={16} />
          {job.salary}
        </span>
        <span>
          <Check size={16} />
          {job.experience_level} years
        </span>
      </div>

      <p className="description">{job.description}</p>
      <div className="skills">{job.skills}</div>

      {isRecruiter && (
        <div className="actions">
          <button onClick={() => onEditJob(job)}>
            <Edit3 size={16} />
            Edit
          </button>
          <button className="danger" onClick={() => onDeleteJob(job.id)}>
            <Trash2 size={16} />
            Delete
          </button>
        </div>
      )}
    </article>
  );
}

createRoot(document.getElementById('root')).render(<App />);
